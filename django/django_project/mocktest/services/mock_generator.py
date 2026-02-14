import random
from typing import Dict, List, Optional, Tuple

from django.apps import apps
from django.db import models, transaction
from django.db.models import Q

from mocktest.models import (
    MockDistributionRule,
    MockTest,
    MockTestQuestion,
    MockTestTab,
)


def _resolve_model(model_name: str):
    if not model_name:
        return None
    try:
        return apps.get_model("bank", model_name)
    except LookupError:
        return None


def _bank_model_choices():
    try:
        return [m._meta.model_name for m in apps.get_app_config("bank").get_models()]
    except LookupError:
        return []


class MockTestGeneratorService:
    """Service to generate/regenerate mocks from distribution rules or manual data."""

    def __init__(self) -> None:
        self.mcq_model = self._get_mcq_model()

    def _get_mcq_model(self):
        try:
            return apps.get_model("bank", "mcq")
        except LookupError:
            try:
                return apps.get_model("bank", "currentaffairs_mcq")
            except LookupError:
                return None

    def _base_queryset(self, model_name: Optional[str] = None):
        target_model = None
        if model_name:
            try:
                target_model = apps.get_model("bank", model_name)
            except LookupError:
                target_model = None
        if target_model is None:
            target_model = self.mcq_model
        if not target_model:
            raise RuntimeError("bank.mcq model not found; cannot generate mock questions.")
        return target_model.objects.all(), target_model

    def _field_exists(self, field: str) -> bool:
        return self.mcq_model and field in {f.name for f in self.mcq_model._meta.get_fields()}  # type: ignore

    def _field_exists_model(self, model, field: str) -> bool:
        return bool(model and field in {f.name for f in model._meta.get_fields()})  # type: ignore

    def _logical_field(self, model, logical: str):
        mapping = {
            "subject": ["subject", "subject_name"],
            "chapter": ["chapter"],
            "sub_chapter": ["sub_chapter"],
            "section": ["section"],
            "difficulty": ["difficulty", "difficult_level"],
            "question": ["question", "question_text", "text"],
        }
        for cand in mapping.get(logical, []):
            if hasattr(model, cand):
                return cand
        return None

    def _filtered_queryset(self, rule: MockDistributionRule):
        qs, model = self._base_queryset(rule.mcq_model)
        def has(field):
            return self._field_exists_model(model, field)

        if rule.subject and has("subject"):
            qs = qs.filter(subject=rule.subject)
        if rule.chapter and has("chapter"):
            qs = qs.filter(chapter=rule.chapter)
        if rule.sub_chapter and has("sub_chapter"):
            qs = qs.filter(sub_chapter=rule.sub_chapter)
        if rule.section and has("section"):
            qs = qs.filter(section=rule.section)
        if rule.question_type and has("question_type"):
            qs = qs.filter(question_type=rule.question_type)
        if rule.difficulty:
            if has("difficulty"):
                qs = qs.filter(difficulty=rule.difficulty)
            elif has("difficult_level"):
                qs = qs.filter(difficult_level=rule.difficulty)
        return qs, model

    def _pick_mcq_ids(self, qs, needed: int, excluded_ids: Optional[List[int]] = None) -> List[int]:
        excluded_ids = excluded_ids or []
        qs = qs.exclude(id__in=excluded_ids)
        if needed <= 0:
            return []
        # Use order_by('?') for simplicity; replace with better sampling if needed
        return list(qs.order_by("?").values_list("id", flat=True)[:needed])

    def _recalc_mock_totals(self, mock: MockTest):
        questions = MockTestQuestion.objects.filter(mock_test=mock)
        mock.total_questions = questions.count()
        aggregate = questions.aggregate(total=models.Sum("marks")) if questions.exists() else {"total": 0}
        mock.total_marks = aggregate.get("total") or 0
        mock.save(update_fields=["total_questions", "total_marks"])

    def _snapshot_config(self, mock: MockTest) -> Dict:
        """Build config snapshot with enriched MCQ info and structured mcq strings."""
        # Collect MCQ ids by model for efficient lookups
        model_to_ids = {}
        fallback_ids = set()
        for tab in mock.tabs.prefetch_related("questions").all():
            for q in tab.questions.all():
                if q.mcq_model:
                    model_to_ids.setdefault(q.mcq_model, set()).add(q.mcq_id)
                else:
                    fallback_ids.add(q.mcq_id)

        mcq_lookup = {}
        # Resolve known models first
        for model_name, ids in model_to_ids.items():
            model = _resolve_model(model_name)
            if not model:
                continue
            question_field = self._logical_field(model, "question")
            subject_field = self._logical_field(model, "subject")
            chapter_field = self._logical_field(model, "chapter")
            sub_chapter_field = self._logical_field(model, "sub_chapter")
            section_field = self._logical_field(model, "section")
            difficulty_field = self._logical_field(model, "difficulty")
            fields = ["id"]
            if self._field_exists_model(model, "new_id"):
                fields.append("new_id")
            for f in [question_field, subject_field, chapter_field, sub_chapter_field, section_field, difficulty_field]:
                if f:
                    fields.append(f)
            for row in model.objects.filter(id__in=ids).values(*fields):
                mcq_lookup[(model_name, row["id"])] = {
                    "model": model._meta.model_name,
                    "id": row["id"],
                    "new_id": row.get("new_id"),
                    "question": row.get(question_field) if question_field else "",
                    "subject": row.get(subject_field) if subject_field else "",
                    "chapter": row.get(chapter_field) if chapter_field else "",
                    "sub_chapter": row.get(sub_chapter_field) if sub_chapter_field else "",
                    "section": row.get(section_field) if section_field else "",
                    "difficulty": row.get(difficulty_field) if difficulty_field else "",
                }

        # Fallback: try all models for ids without stored model
        if fallback_ids:
            for model_name in _bank_model_choices():
                model = _resolve_model(model_name)
                if not model:
                    continue
                question_field = self._logical_field(model, "question")
                subject_field = self._logical_field(model, "subject")
                chapter_field = self._logical_field(model, "chapter")
                sub_chapter_field = self._logical_field(model, "sub_chapter")
                section_field = self._logical_field(model, "section")
                difficulty_field = self._logical_field(model, "difficulty")
                fields = ["id"]
                if self._field_exists_model(model, "new_id"):
                    fields.append("new_id")
                for f in [question_field, subject_field, chapter_field, sub_chapter_field, section_field, difficulty_field]:
                    if f:
                        fields.append(f)
                for row in model.objects.filter(id__in=fallback_ids).values(*fields):
                    key = (model_name, row["id"])
                    if key in mcq_lookup:
                        continue
                    mcq_lookup[key] = {
                        "model": model._meta.model_name,
                        "id": row["id"],
                        "new_id": row.get("new_id"),
                        "question": row.get(question_field) if question_field else "",
                        "subject": row.get(subject_field) if subject_field else "",
                        "chapter": row.get(chapter_field) if chapter_field else "",
                        "sub_chapter": row.get(sub_chapter_field) if sub_chapter_field else "",
                        "section": row.get(section_field) if section_field else "",
                        "difficulty": row.get(difficulty_field) if difficulty_field else "",
                    }

        tabs_payload = []
        for tab in mock.tabs.prefetch_related("distribution_rules", "questions").all():
            tab_info = {
                "tab_id": tab.id,
                "tab_name": tab.tab.name,
                "selection_mode": tab.selection_mode,
                "total_questions": tab.total_questions,
                "time_limit_minutes": tab.time_limit_minutes,
                "order": tab.order,
                "mcqs": [],
            }
            tab_info["mcq_details"] = []
            questions = list(tab.questions.all().order_by("order", "id"))
            for q in questions:
                resolved_model = q.mcq_model
                resolved_key = None
                if resolved_model:
                    resolved_key = (resolved_model, q.mcq_id)
                    resolved_model = resolved_model.strip()
                else:
                    # Try to find a unique match across lookups
                    matches = [(m, mid) for (m, mid) in mcq_lookup.keys() if mid == q.mcq_id]
                    if len(matches) == 1:
                        resolved_key = matches[0]
                        resolved_model = matches[0][0]
                    else:
                        resolved_model = resolved_model or ""

                mcq_info = mcq_lookup.get(resolved_key) if resolved_key else None
                new_id = mcq_info.get("new_id") if mcq_info else None
                if new_id:
                    mcq_string = f"{resolved_model}$$${q.mcq_id}$$${new_id}"
                else:
                    mcq_string = f"{resolved_model}$$${q.mcq_id}"
                tab_info["mcqs"].append(mcq_string)

                # Use stored question metadata (no /mocktest/mocktestquestion dependency)
                details_entry = {
                    "mcq_model": q.mcq_model or (resolved_model or ""),
                    "mcq_id": q.mcq_id,
                    "marks": q.marks,
                    "negative_marks": q.negative_marks,
                    "order": q.order,
                }
                tab_info["mcq_details"].append(details_entry)
            tabs_payload.append(tab_info)

        return {
            "mocktest": {
                "id": mock.id,
                "title": getattr(mock, "title", None),
                "exam": getattr(mock, "exam", None),
                "mock_type": getattr(mock, "mock_type", None),
            },
            "tabs": tabs_payload,
        }

    def _update_config_snapshot(self, mock: MockTest):
        """Persist a fresh config_json snapshot for the given mock."""
        mock.config_json = self._snapshot_config(mock)
        mock.save(update_fields=["config_json"])

    @transaction.atomic
    def generate_mock(self, mock_test_id: int):
        mock = MockTest.objects.select_for_update().get(id=mock_test_id)
        # Remove only auto-generated questions; keep manual additions
        MockTestQuestion.objects.filter(mock_test=mock, added_manually=False).delete()
        for tab in mock.tabs.all():
            self._generate_tab(tab)
        self._update_config_snapshot(mock)

    @transaction.atomic
    def regenerate_tab(self, mock_test_tab_id: int):
        tab = MockTestTab.objects.select_for_update().get(id=mock_test_tab_id)
        self._generate_tab(tab)
        mock = tab.mock_test
        self._update_config_snapshot(mock)

    def update_config_from_existing(self, mock_test_id: int):
        """Refresh config_json using current questions/rules without repicking."""
        mock = MockTest.objects.get(id=mock_test_id)
        self._update_config_snapshot(mock)

    def _generate_tab(self, tab: MockTestTab):
        if tab.selection_mode != "auto":
            return

        MockTestQuestion.objects.filter(mock_test_tab=tab, added_manually=False).delete()
        rules = list(tab.distribution_rules.all())
        # Prioritize by specificity: section > sub_chapter > chapter > subject
        rules.sort(key=lambda r: (
            1 if r.section else 0,
            1 if r.sub_chapter else 0,
            1 if r.chapter else 0,
        ), reverse=True)

        selected_ids: List[int] = list(
            MockTestQuestion.objects.filter(mock_test_tab=tab).values_list("mcq_id", flat=True)
        )
        order_cursor = MockTestQuestion.objects.filter(mock_test_tab=tab).aggregate(max_order=models.Max("order"))["max_order"] or 0

        for rule in rules:
            target = rule.question_count or 0
            if not target and rule.percentage:
                target = int((rule.percentage / 100.0) * (tab.total_questions or 0))
            qs, model = self._filtered_queryset(rule)
            picked = self._pick_mcq_ids(qs, target, excluded_ids=selected_ids)
            for mcq_id in picked:
                order_cursor += 1
                MockTestQuestion.objects.create(
                    mock_test=tab.mock_test,
                    mock_test_tab=tab,
                    mcq_model=model._meta.model_name if model else None,
                    mcq_id=mcq_id,
                    order=order_cursor,
                    marks=1.0,
                    negative_marks=0.0,
                    added_manually=False,
                )
            # Update rule tracking to match freshly picked MCQs
            if picked:
                rule.selected_mcq_ids = list(picked)
                rule.mcq_list = ",".join(str(mid) for mid in picked)
                rule.save(update_fields=["selected_mcq_ids", "mcq_list"])
            selected_ids.extend(picked)

        # Do not overwrite configured tab total; leave total_questions as user-set cap.

    def validate_distribution(self, mock_test_id: int) -> List[str]:
        issues: List[str] = []
        mock = MockTest.objects.get(id=mock_test_id)
        for tab in mock.tabs.prefetch_related("distribution_rules"):
            if tab.selection_mode != "auto":
                continue
            total_percentage = 0.0
            total_explicit = 0
            for rule in tab.distribution_rules.all():
                if not rule.question_count and not rule.percentage:
                    issues.append(f"Tab {tab.id}: rule missing count/percentage")
                if rule.percentage:
                    total_percentage += rule.percentage
                if rule.question_count:
                    total_explicit += rule.question_count
                if rule.percentage and rule.question_count:
                    issues.append(f"Tab {tab.id}: rule has both count and percentage")
            if total_percentage > 100.0:
                issues.append(f"Tab {tab.id}: percentage total exceeds 100 ({total_percentage})")
            if total_explicit > tab.total_questions and tab.total_questions:
                issues.append(f"Tab {tab.id}: explicit counts exceed tab total")
        return issues


def _parse_mcq_string(raw: str) -> Tuple[str, Optional[int], Optional[str]]:
    """Split an mcq token of form `model$$$id$$$new_id`.

    Returns (model, id|None, new_id|None) with model stripped. Safe for
    2-part entries that omit new_id.
    """

    parts = (raw or "").split("$$$")
    if not parts:
        return "", None, None

    model = (parts[0] or "").strip()
    mcq_id: Optional[int] = None
    new_id: Optional[str] = None

    if len(parts) > 1 and parts[1]:
        try:
            mcq_id = int(parts[1])
        except (TypeError, ValueError):
            mcq_id = None

    if len(parts) > 2 and parts[2]:
        new_id = parts[2]

    return model, mcq_id, new_id


# Known field hints across MCQ models
OPTION_TEXT_FIELDS = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "option_1",
    "option_2",
    "option_3",
    "option_4",
    "option_5",
]

OPTION_IMAGE_FIELDS = [
    "a_img",
    "b_img",
    "c_img",
    "d_img",
    "e_img",
    "f_img",
    "g_img",
    "h_img",
    "i_img",
    "j_img",
]

QUESTION_IMAGE_FIELDS = [
    "question_image",
    "one",
    "two",
    "three",
    "four",
    "five",
]

SOLUTION_IMAGE_FIELDS = [
    "solution_image",
    "solution_one",
    "solution_two",
    "solution_three",
    "solution_four",
    "solution_five",
]


def _available(model, names: List[str]) -> List[str]:
    return [n for n in names if hasattr(model, n)]


def _collect_fieldset(model) -> Dict[str, List[str]]:
    """Return field names grouped by purpose for a given model."""

    return {
        "question": [n for n in ["question"] if hasattr(model, n)],
        "question_part": [n for n in ["question_part"] if hasattr(model, n)],
        "question_images": _available(model, QUESTION_IMAGE_FIELDS),
        "options": _available(model, OPTION_TEXT_FIELDS),
        "option_images": _available(model, OPTION_IMAGE_FIELDS),
        "solution": [n for n in ["solution"] if hasattr(model, n)],
        "solution_images": _available(model, SOLUTION_IMAGE_FIELDS),
        "shortcut": [n for n in ["shortcut"] if hasattr(model, n)],
        "shortcut_image": [n for n in ["shortcut_image"] if hasattr(model, n)],
        "answer": [n for n in ["ans", "answer"] if hasattr(model, n)],
        "time": [n for n in ["time"] if hasattr(model, n)],
        "question_type": [n for n in ["question_type"] if hasattr(model, n)],
        "difficulty": [n for n in ["difficult_level", "difficulty", "level"] if hasattr(model, n)],
        "subject": [n for n in ["subject", "subject_name"] if hasattr(model, n)],
        "chapter": [n for n in ["chapter"] if hasattr(model, n)],
        "sub_chapter": [n for n in ["sub_chapter"] if hasattr(model, n)],
        "section": [n for n in ["section"] if hasattr(model, n)],
        "extra": [n for n in ["extra"] if hasattr(model, n)],
        "new_id": [n for n in ["new_id"] if hasattr(model, n)],
    }


def resolve_config_mcqs(config: Dict) -> Dict:
    """Resolve MCQ details for a config JSON using bulk queries (new_id preferred).

    This consumes the cached/live mocktest config and returns a new payload with
    each tab extended by `mcq_records`, where every record contains the fetched
    MCQ fields. Lookup order per MCQ: new_id (when present) first, else id. One
    query per distinct model; no per-row queries.
    """

    tabs = config.get("tabs", []) or []
    if not tabs:
        return {**config, "tabs": []}

    # Build aggregated lookup sets per model
    requested: Dict[str, Dict[str, set]] = {}
    for tab in tabs:
        for raw in tab.get("mcqs", []) or []:
            model, mcq_id, new_id = _parse_mcq_string(raw)
            if not model:
                continue
            bucket = requested.setdefault(model, {"ids": set(), "new_ids": set()})
            if mcq_id is not None:
                bucket["ids"].add(mcq_id)
            if new_id:
                bucket["new_ids"].add(new_id)

    # Bulk fetch per model
    generator = MockTestGeneratorService()
    by_id: Dict[Tuple[str, int], Dict] = {}
    by_new_id: Dict[Tuple[str, str], Dict] = {}

    for model_name, filters in requested.items():
        model = _resolve_model(model_name)
        if not model:
            continue

        fieldset = _collect_fieldset(model)
        has_new_id = bool(fieldset.get("new_id"))

        if not filters.get("ids") and not (has_new_id and filters.get("new_ids")):
            continue

        # Build fields to fetch
        fields: List[str] = ["id"]
        for group in fieldset.values():
            fields.extend(group)

        q_filter = Q()
        if filters.get("ids"):
            q_filter |= Q(id__in=filters["ids"])
        if has_new_id and filters.get("new_ids"):
            q_filter |= Q(new_id__in=filters["new_ids"])

        if not q_filter.children:
            continue

        for row in model.objects.filter(q_filter).values(*fields):
            # Extract question/difficulty/subject fields via logical mapping fallback
            question = row.get(fieldset["question"][0]) if fieldset["question"] else ""
            question_part = row.get(fieldset["question_part"][0]) if fieldset["question_part"] else None
            difficulty_val = None
            for f in fieldset["difficulty"]:
                if row.get(f) is not None:
                    difficulty_val = row.get(f)
                    break

            def collect_list(names: List[str]) -> List:
                return [row.get(n) for n in names if row.get(n) not in (None, "")]

            option_texts = collect_list(fieldset["options"])
            option_images = collect_list(fieldset["option_images"])
            question_images = collect_list(fieldset["question_images"])
            solution_images = collect_list(fieldset["solution_images"])

            answer_val = None
            for f in fieldset["answer"]:
                if row.get(f) is not None:
                    answer_val = row.get(f)
                    break

            payload = {
                "mcq_model": model._meta.model_name,
                "mcq_id": row["id"],
                "new_id": row.get("new_id"),
                "question": question,
                "question_part": question_part,
                "question_images": question_images,
                "options": option_texts,
                "option_images": option_images,
                "answer": answer_val,
                "solution": row.get(fieldset["solution"][0]) if fieldset["solution"] else None,
                "solution_images": solution_images,
                "shortcut": row.get(fieldset["shortcut"][0]) if fieldset["shortcut"] else None,
                "shortcut_image": row.get(fieldset["shortcut_image"][0]) if fieldset["shortcut_image"] else None,
                "subject": row.get(fieldset["subject"][0]) if fieldset["subject"] else None,
                "chapter": row.get(fieldset["chapter"][0]) if fieldset["chapter"] else None,
                "sub_chapter": row.get(fieldset["sub_chapter"][0]) if fieldset["sub_chapter"] else None,
                "section": row.get(fieldset["section"][0]) if fieldset["section"] else None,
                "difficulty": difficulty_val,
                "question_type": row.get(fieldset["question_type"][0]) if fieldset["question_type"] else None,
                "time": row.get(fieldset["time"][0]) if fieldset["time"] else None,
                "extra": row.get(fieldset["extra"][0]) if fieldset["extra"] else None,
            }

            by_id[(model_name, row["id"])] = payload
            if has_new_id and row.get("new_id"):
                by_new_id[(model_name, row["new_id"])] = payload

    # Enrich tabs with resolved records (preserving order from config.mcqs)
    resolved_tabs: List[Dict] = []
    for tab in tabs:
        details_lookup = {
            (d.get("mcq_model"), d.get("mcq_id")): d
            for d in (tab.get("mcq_details") or [])
        }
        records = []
        for raw in tab.get("mcqs", []) or []:
            model, mcq_id, new_id = _parse_mcq_string(raw)
            chosen = None
            if model and new_id and (model, new_id) in by_new_id:
                chosen = by_new_id[(model, new_id)]
            elif model and mcq_id is not None and (model, mcq_id) in by_id:
                chosen = by_id[(model, mcq_id)]

            # Merge with marks/order metadata when available
            detail = details_lookup.get((model, mcq_id), {})

            record = {
                "mcq_model": model,
                "mcq_id": mcq_id,
                "new_id": new_id,
                "found": bool(chosen),
                "question": chosen.get("question") if chosen else None,
                "question_part": chosen.get("question_part") if chosen else None,
                "question_images": chosen.get("question_images") if chosen else [],
                "options": chosen.get("options") if chosen else [],
                "option_images": chosen.get("option_images") if chosen else [],
                "answer": chosen.get("answer") if chosen else None,
                "solution": chosen.get("solution") if chosen else None,
                "solution_images": chosen.get("solution_images") if chosen else [],
                "shortcut": chosen.get("shortcut") if chosen else None,
                "shortcut_image": chosen.get("shortcut_image") if chosen else None,
                "subject": chosen.get("subject") if chosen else None,
                "chapter": chosen.get("chapter") if chosen else None,
                "sub_chapter": chosen.get("sub_chapter") if chosen else None,
                "section": chosen.get("section") if chosen else None,
                "difficulty": chosen.get("difficulty") if chosen else None,
                "question_type": chosen.get("question_type") if chosen else None,
                "time": chosen.get("time") if chosen else None,
                "extra": chosen.get("extra") if chosen else None,
                "marks": detail.get("marks"),
                "negative_marks": detail.get("negative_marks"),
                "order": detail.get("order"),
            }
            records.append(record)

        resolved_tab = {**tab}
        resolved_tab["mcq_records"] = records
        resolved_tabs.append(resolved_tab)

    return {**config, "tabs": resolved_tabs}
