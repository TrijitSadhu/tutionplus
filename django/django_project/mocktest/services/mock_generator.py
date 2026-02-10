import random
from typing import Dict, List, Optional

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
