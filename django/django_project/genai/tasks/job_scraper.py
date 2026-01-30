import logging
import re
import json
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover - playright is required per design, but guard for runtime safety
    sync_playwright = None

from bank.models import job as JobModel
from genai.utils.llm_provider import default_llm

logger = logging.getLogger(__name__)


def _log(message: str) -> None:
    """Mirror messages to stdout and logger for live visibility."""
    print(message, flush=True)
    logger.info(message)

LISTING_URL_FREEJOBALERT = "https://www.freejobalert.com/latest-notifications/"
CONF_HIGH = Decimal("0.95")
CONF_MED = Decimal("0.80")
CONF_LOW = Decimal("0.60")
MAX_LLM_HTML_CHARS = 15000  # guard to keep payload under provider limits


def download_url(url: str, wait_ms: int = 1500, timeout_ms: int = 20000) -> str:
    """Generic Playwright downloader. Handles JS/redirects; no site logic."""
    if sync_playwright is None:
        raise RuntimeError("Playwright is not installed; please add playwright and browsers.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=timeout_ms)
        page.wait_for_timeout(wait_ms)
        html = page.content()
        browser.close()
        return html


def _safe_text(node) -> str:
    return node.get_text(strip=True) if node else ""


def _parse_date(text: str) -> Optional[datetime.date]:
    print(f"_parse_date input: '{text}'")
    if not text:
        return None
    cleaned = text.strip()
    print(f"_parse_date cleaned: '{cleaned}'")
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d %b %Y", "%d %B %Y","%d %B %Y","%Y-%m-%d"):
        try:
            print(f"Trying format: {fmt}")
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue
    # Try to locate a 4-digit year; fall back to year-only
    year_match = re.search(r"(20\d{2})", cleaned)
    if year_match:
        try:
            return datetime.strptime(year_match.group(1), "%Y").date()
        except ValueError:
            return None
    return None


def _extract_year(*candidates: str) -> Optional[str]:
    for cand in candidates:
        if not cand:
            continue
        match = re.search(r"(20\d{2})", cand)
        if match:
            return match.group(1)
    return None


def _collect_table_fields(detail_soup: BeautifulSoup) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    for row in detail_soup.select("table tr"):
        cells = row.find_all(["td", "th"])
        if len(cells) < 2:
            continue
        key = _safe_text(cells[0])
        val = _safe_text(cells[1])
        if key:
            fields[key] = val
    return fields


def _extract_detail_fields(detail_soup: BeautifulSoup) -> Dict[str, Optional[str]]:
    content = detail_soup.select_one(".entry-content") or detail_soup
    authority = _safe_text(detail_soup.select_one("h1"))
    post_name = _safe_text(content.select_one("strong")) or _safe_text(content.select_one("b"))

    table_fields = _collect_table_fields(detail_soup)
    advt_no = None
    exam_code = None
    last_date = None
    eligibility_text = None

    for key, val in table_fields.items():
        low = key.lower()
        if re.search(r"advt|advertisement|notification", low):
            advt_no = val
        elif re.search(r"exam|cen", low):
            exam_code = val
        elif "last date" in low:
            last_date = val
        elif re.search(r"qualification|eligibility", low):
            eligibility_text = val

    return {
        "authority": authority,
        "post_name": post_name,
        "advt_no": advt_no,
        "exam_code": exam_code,
        "last_date": last_date,
        "eligibility_text": eligibility_text,
        "content": content,
    }


def _build_canonical(board: Optional[str], post_name: Optional[str], post_date: Optional[datetime.date], last_date: Optional[str]) -> Optional[str]:
    """Unified canonical: board + post_name + post_date + last_date (consistent across stages)."""
    if not post_name:
        return None

    # Normalize dates to ISO strings when possible
    post_date_str: Optional[str]
    if isinstance(post_date, datetime):
        post_date_str = post_date.date().isoformat()
    elif hasattr(post_date, "isoformat"):
        post_date_str = post_date.isoformat()  # type: ignore[attr-defined]
    elif isinstance(post_date, str) and post_date.strip():
        parsed_pd = _parse_date(post_date)
        post_date_str = parsed_pd.isoformat() if parsed_pd else post_date.strip()
    else:
        post_date_str = None

    last_date_str: Optional[str]
    if isinstance(last_date, datetime):
        last_date_str = last_date.date().isoformat()
    elif hasattr(last_date, "isoformat"):
        last_date_str = last_date.isoformat()  # type: ignore[attr-defined]
    elif isinstance(last_date, str) and last_date.strip():
        parsed_ld = _parse_date(last_date)
        last_date_str = parsed_ld.isoformat() if parsed_ld else last_date.strip()
    else:
        last_date_str = None

    parts: List[str] = []
    if board:
        parts.append(board)
    parts.append(post_name)
    if post_date_str:
        parts.append(post_date_str)
    if last_date_str:
        parts.append(last_date_str)

    return "::".join(parts) if parts else None


def _build_canonical_pre(board: Optional[str], post_name: Optional[str], post_date: Optional[datetime.date], last_date: Optional[str]) -> Optional[str]:
    return _build_canonical(board, post_name, post_date, last_date)


def _build_canonical_from_llm(data: Dict[str, Optional[str]], board: Optional[str], post_date: Optional[datetime.date]) -> Tuple[Optional[str], Optional[Decimal]]:
    post_name = data.get("post_name")
    last_date = data.get("last_date")
    canonical = _build_canonical(board, post_name, post_date, last_date)
    if canonical:
        # Confidence tiers: both dates present => high; only one date => medium; otherwise low
        has_post_date = post_date is not None
        has_last_date = bool(last_date)
        if has_post_date and has_last_date:
            return canonical, CONF_HIGH
        if has_post_date or has_last_date:
            return canonical, CONF_MED
        return canonical, CONF_LOW
    return None, None


def _build_canonical_from_listing(board: Optional[str], post_name: Optional[str], post_date: Optional[datetime.date], last_date: Optional[str]) -> Optional[str]:
    """Build a pre-detail canonical id using listing fields (board + post_name + post_date + last_date)."""
    return _build_canonical(board, post_name, post_date, last_date)


def _collect_other_info_html(content: BeautifulSoup) -> str:
    if not content:
        return ""
    snippets: List[str] = []
    keywords = ["selection", "exam pattern", "instruction", "note"]
    for node in content.find_all(["h2", "h3", "strong", "b", "p", "li", "div"]):
        text = node.get_text(" ", strip=True).lower()
        if any(kw in text for kw in keywords):
            # Prefer the parent block if it adds context
            target = node.parent if node.parent and node.parent.name in ["p", "div", "li"] else node
            html_piece = str(target)
            if html_piece not in snippets:
                snippets.append(html_piece)
    return "\n".join(snippets)


def _prune_html_for_llm(html_detail: str) -> str:
    soup = BeautifulSoup(html_detail, "html.parser")

    for tag in soup.select("script, style, nav, footer, header, aside"):
        tag.decompose()

    main = soup.select_one(".entry-content") or soup.select_one("article") or soup.body or soup

    fragments: List[str] = []

    # Always include tables
    for tbl in main.find_all("table"):
        fragments.append(str(tbl))
        if sum(len(f) for f in fragments) > MAX_LLM_HTML_CHARS:
            break

    # Keep key sections with eligibility/age/fee/important date words
    keywords = ["eligibility", "qualification", "age", "fee", "important", "selection", "instruction"]
    for node in main.find_all(["h1", "h2", "h3", "p", "li", "div", "strong", "b"]):
        text_low = node.get_text(" ", strip=True).lower()
        if any(kw in text_low for kw in keywords):
            frag = str(node if node.name in ["table"] else node)
            fragments.append(frag)
        if sum(len(f) for f in fragments) > MAX_LLM_HTML_CHARS:
            break

    # Fallback: first 40 paragraphs/headings for context
    if sum(len(f) for f in fragments) < MAX_LLM_HTML_CHARS:
        count = 0
        for node in main.find_all(["h1", "h2", "h3", "p", "li"]):
            frag = str(node)
            fragments.append(frag)
            count += 1
            if count >= 40 or sum(len(f) for f in fragments) > MAX_LLM_HTML_CHARS:
                break

    pruned = "\n".join(fragments)
    return pruned[:MAX_LLM_HTML_CHARS]


def _normalized_category(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    lowered = raw.strip().lower()
    valid = {c[0] for c in JobModel._meta.get_field("category").choices}
    if lowered in valid:
        return lowered
    return None


def _normalized_state(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    lowered = raw.strip().lower().replace(" ", "_")
    valid = {c[0] for c in JobModel._meta.get_field("state").choices}
    return lowered if lowered in valid else None


def _apply_llm(html_detail: str, llm_prompt_text: str, prune_html: bool) -> Dict[str, str]:
    if not default_llm:
        raise RuntimeError("LLM provider is not configured.")
    html_for_llm = _prune_html_for_llm(html_detail) if prune_html else html_detail
    truncated_html = html_for_llm[:MAX_LLM_HTML_CHARS]
    payload = f"{llm_prompt_text}\n\nRAW_HTML (truncated to {MAX_LLM_HTML_CHARS} chars):\n{truncated_html}\n\nReturn JSON with fields authority, post_name, advt_no, exam_code, first_day, last_day, eligibility, age, amount, apply_link, category, state, other_info."
    response = default_llm.generate_json(payload)
    if not isinstance(response, dict):
        raise ValueError("LLM response was not JSON object")
   
    return response


def _job_exists(canonical_id: Optional[str]) -> bool:
    if not canonical_id:
        return False
    return JobModel.objects.filter(canonical_id=canonical_id).exists()


def _save_job(data: Dict[str, Optional[str]], canonical_id: Optional[str], canonical_conf: Optional[Decimal], detail_link: str) -> JobModel:
    obj = JobModel(
        heading=data.get("authority")+":"+(data.get("post_name") or data.get("listing_post_name") or data.get("authority") or ""),
        first_day=_parse_date(data.get("first_day") or "") or datetime.today().date(),
        last_day=_parse_date(data.get("last_day") or data.get("listing_last_date") or "") or datetime.today().date(),
        eligibility=data.get("eligibility") or data.get("eligibility_text") or "",
        age=data.get("age") or "",
        amount=data.get("amount") or "",
        apply_link=data.get("apply_link") or detail_link or "",
        category=_normalized_category(data.get("category")) or "other",
        state=_normalized_state(data.get("state")) or "any",
        detail_link=detail_link or "",
        canonical_id=canonical_id,
        canonical_confidence=canonical_conf,
        other_info=data.get("other_info") or "",
        graduate_only=bool(data.get("graduate_only")),
        tenth=bool(data.get("tenth")),
        twelth=bool(data.get("twelth")),
        eighth=bool(data.get("eighth")),
        iti=bool(data.get("iti")),
        deploma=bool(data.get("deploma")),
        b_com=bool(data.get("b_com")),
        b_ed=bool(data.get("b_ed")),
        b_pharm=bool(data.get("b_pharm")),
        b_sc=bool(data.get("b_sc")),
        bba=bool(data.get("bba")),
        bca=bool(data.get("bca")),
        bds=bool(data.get("bds")),
        b_tech=bool(data.get("b_tech")),
        ca=bool(data.get("ca")),
        cs=bool(data.get("cs")),
        llb=bool(data.get("llb")),
        llm=bool(data.get("llm")),
        m_com=bool(data.get("m_com")),
        m_ed=bool(data.get("m_ed")),
        m_pharm=bool(data.get("m_pharm")),
        m_sc=bool(data.get("m_sc")),
        mba=bool(data.get("mba")),
        mca=bool(data.get("mca")),
        m_tech=bool(data.get("m_tech")),
        mbbs=bool(data.get("mbbs")),
        medical=bool(data.get("medical")),
        agriculture=bool(data.get("agriculture")),
        phd=bool(data.get("phd")),
        m_phil=bool(data.get("m_phil")),
        post_g=bool(data.get("post_g")),
    )
    print(f"Saving job: {obj.apply_link}")
    obj.save()
    return obj


def scrape_freejobalert(max_jobs_to_fetch: int, llm_prompt_text: str, use_llm: bool, prune_html: bool) -> Dict[str, int]:
    _log("[JOBFETCH] Starting freejobalert scrape")
    _log(f"[JOBFETCH] Params max_jobs={max_jobs_to_fetch} use_llm={use_llm} prune_html={prune_html}")
    summary = {
        "list_rows": 0,
        "details_fetched": 0,
        "llm_calls": 0,
        "inserted": 0,
        "duplicates": 0,
        "errors": 0,
    }
    listing_html = download_url(LISTING_URL_FREEJOBALERT)
    _log(f"[JOBFETCH] Listing downloaded from {LISTING_URL_FREEJOBALERT}")
    soup = BeautifulSoup(listing_html, "html.parser")
    rows = soup.select("table tbody tr")
    summary["list_rows"] = len(rows)
    _log(f"[JOBFETCH] Found {summary['list_rows']} listing rows")

    for idx, row in enumerate(rows, 1):
        if max_jobs_to_fetch and summary["details_fetched"] >= max_jobs_to_fetch:
            _log(f"[JOBFETCH] Reached max_jobs limit ({max_jobs_to_fetch}), stopping")
            break

        listing_post_date_raw = _safe_text(row.select_one("td:nth-of-type(1)"))
        listing_post_date = _parse_date(listing_post_date_raw)
        listing_board = _safe_text(row.select_one("td:nth-of-type(2)"))
        listing_post_name = _safe_text(row.select_one("td:nth-of-type(3)"))
        listing_qualification = _safe_text(row.select_one("td:nth-of-type(4)"))
        listing_last_date_raw = _safe_text(row.select_one("td:nth-of-type(6)"))
        listing_last_date = _parse_date(listing_last_date_raw)
        link_node = row.select_one("td:nth-of-type(7) a")
        listing_detail_link = link_node["href"] if link_node and link_node.has_attr("href") else ""

        listing_canonical = _build_canonical_from_listing(listing_board, listing_post_name, listing_post_date, listing_last_date or listing_last_date_raw)
        _log(f"[JOBFETCH] Row {idx}: listing canonical candidate = {listing_canonical}")
        if listing_canonical and _job_exists(listing_canonical):
            summary["duplicates"] += 1
            _log(f"[JOBFETCH] Row {idx}: listing duplicate detected (canonical {listing_canonical}); skipping before detail fetch")
            continue

        if not listing_detail_link:
            summary["errors"] += 1
            _log(f"[JOBFETCH] Row {idx}: missing detail link; skipping. Listing data => board={listing_board}, post_name={listing_post_name}, post_date={listing_post_date_raw or listing_post_date}, last_date={listing_last_date_raw or listing_last_date}")
            continue

        try:
            _log(
                f"[JOBFETCH] Row {idx}: fetching detail {listing_detail_link} | "
                f"board={listing_board}, post_name={listing_post_name}, post_date={listing_post_date_raw or listing_post_date}, "
                f"last_date={listing_last_date_raw or listing_last_date}, qualification={listing_qualification}"
            )
            detail_html = download_url(listing_detail_link)
            summary["details_fetched"] += 1
            _log(f"[JOBFETCH] Row {idx}: detail fetched")
            detail_soup = BeautifulSoup(detail_html, "html.parser")
            pre = _extract_detail_fields(detail_soup)
            canonical_last_date = listing_last_date or listing_last_date_raw or pre.get("last_date")
            pre_key = _build_canonical_pre(
                listing_board,
                pre.get("post_name") or listing_post_name,
                listing_post_date,
                canonical_last_date,
            )
            _log(f"[JOBFETCH] Row {idx}: pre canonical candidate = {pre_key}")
            if pre_key and _job_exists(pre_key):
                summary["duplicates"] += 1
                _log(f"[JOBFETCH] Row {idx}: duplicate detected (pre canonical {pre_key}); skipping")
                continue

            # Decide whether to call LLM
            llm_data: Dict[str, Optional[str]] = {}
            if use_llm:
                _log(f"[JOBFETCH] Row {idx}: calling LLM (prune_html={prune_html})")
                llm_data = _apply_llm(detail_html, llm_prompt_text, prune_html)
                # print("llm_data")
                # print(llm_data)
                summary["llm_calls"] += 1
                _log(f"[JOBFETCH] Row {idx}: LLM returned")
                try:
                    _log(f"[JOBFETCH] Row {idx}: LLM JSON = {json.dumps(llm_data, ensure_ascii=True)}")
                except Exception:
                    _log(f"[JOBFETCH] Row {idx}: LLM JSON (raw) = {llm_data}")
            else:
                llm_data = {}

            # Merge deterministic fields with LLM output
            merged: Dict[str, Optional[str]] = {
                "listing_post_name": listing_post_name,
                "listing_post_date": listing_post_date.isoformat() if listing_post_date else listing_post_date_raw,
                "listing_board": listing_board,
                "listing_qualification": listing_qualification,
                "listing_last_date": listing_last_date.isoformat() if listing_last_date else listing_last_date_raw,
                "authority": llm_data.get("authority") if llm_data else pre.get("authority"),
                "post_name": llm_data.get("post_name") if llm_data else (pre.get("post_name") or listing_post_name),
                "advt_no": llm_data.get("advt_no") if llm_data else pre.get("advt_no"),
                "exam_code": llm_data.get("exam_code") if llm_data else pre.get("exam_code"),
                "first_day": llm_data.get("first_day") if llm_data else None,
                "last_day": llm_data.get("last_day") if llm_data else pre.get("last_date"),
                "eligibility": llm_data.get("eligibility") if llm_data else pre.get("eligibility_text"),
                "eligibility_text": pre.get("eligibility_text"),
                "age": llm_data.get("age") if llm_data else None,
                "amount": llm_data.get("amount") if llm_data else None,
                "apply_link": llm_data.get("apply_link") if llm_data else listing_detail_link,
                "category": llm_data.get("category") if llm_data else None,
                "state": llm_data.get("state") if llm_data else None,
                "other_info": llm_data.get("other_info") if llm_data else _collect_other_info_html(pre.get("content")),
                "graduate_only": llm_data.get("graduate_only") if llm_data else None,
                "tenth": llm_data.get("tenth") if llm_data else None,
                "twelth": llm_data.get("twelth") if llm_data else None,
                "eighth": llm_data.get("eighth") if llm_data else None,
                "iti": llm_data.get("iti") if llm_data else None,
                "deploma": llm_data.get("deploma") if llm_data else None,
                "b_com": llm_data.get("b_com") if llm_data else None,
                "b_ed": llm_data.get("b_ed") if llm_data else None,
                "b_pharm": llm_data.get("b_pharm") if llm_data else None,
                "b_sc": llm_data.get("b_sc") if llm_data else None,
                "bba": llm_data.get("bba") if llm_data else None,
                "bca": llm_data.get("bca") if llm_data else None,
                "bds": llm_data.get("bds") if llm_data else None,
                "b_tech": llm_data.get("b_tech") if llm_data else None,
                "ca": llm_data.get("ca") if llm_data else None,
                "cs": llm_data.get("cs") if llm_data else None,
                "llb": llm_data.get("llb") if llm_data else None,
                "llm": llm_data.get("llm") if llm_data else None,
                "m_com": llm_data.get("m_com") if llm_data else None,
                "m_ed": llm_data.get("m_ed") if llm_data else None,
                "m_pharm": llm_data.get("m_pharm") if llm_data else None,
                "m_sc": llm_data.get("m_sc") if llm_data else None,
                "mba": llm_data.get("mba") if llm_data else None,
                "mca": llm_data.get("mca") if llm_data else None,
                "m_tech": llm_data.get("m_tech") if llm_data else None,
                "mbbs": llm_data.get("mbbs") if llm_data else None,
                "medical": llm_data.get("medical") if llm_data else None,
                "agriculture": llm_data.get("agriculture") if llm_data else None,
                "phd": llm_data.get("phd") if llm_data else None,
                "m_phil": llm_data.get("m_phil") if llm_data else None,
                "post_g": llm_data.get("post_g") if llm_data else None,
            }

            canonical_id, canonical_conf = _build_canonical_from_llm(
                {
                    #"post_name": merged.get("post_name"),
                    "post_name":listing_post_name,
                    "last_date": merged.get("listing_last_date") or merged.get("last_day"),
                },
                listing_board,
                listing_post_date,
            )
            _log(f"[JOBFETCH] Row {idx}: final canonical candidate = {canonical_id} conf={canonical_conf}")

            if _job_exists(canonical_id):
                summary["duplicates"] += 1
                _log(f"[JOBFETCH] Row {idx}: duplicate detected (LLM canonical {canonical_id}); skipping")
                continue

            _save_job(merged, canonical_id, canonical_conf, listing_detail_link)
            summary["inserted"] += 1
            _log(f"[JOBFETCH] Row {idx}: saved job with canonical={canonical_id} conf={canonical_conf}")
        except Exception as exc:  # pragma: no cover - runtime safety
            logger.exception("Error processing job row %s", idx)
            summary["errors"] += 1
            _log(f"[JOBFETCH] Row {idx}: error {exc}")
            continue

    _log(f"[JOBFETCH] Done. Summary: {summary}")
    return summary


def run_job_fetch(site_identifier: str, max_jobs_to_fetch: int, llm_prompt_text: str, use_llm: bool, prune_html: bool = True) -> Dict[str, int]:
    _log(f"[JOBFETCH] Dispatch run_job_fetch site={site_identifier}")
    if site_identifier == "freejobalert":
        return scrape_freejobalert(max_jobs_to_fetch, llm_prompt_text, use_llm, prune_html)
    raise ValueError(f"Unsupported site identifier: {site_identifier}")
