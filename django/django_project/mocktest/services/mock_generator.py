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

    def _filtered_queryset(self, rule: MockDistributionRule):
        qs, model = self._base_queryset(rule.mcq_model)
        def has(field):
            return self._field_exists_model(model, field)

        if has("subject"):
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
        tabs_payload = []
        for tab in mock.tabs.prefetch_related("distribution_rules").all():
            tab_info = {
                "tab_id": tab.id,
                "tab_name": tab.tab.name,
                "selection_mode": tab.selection_mode,
                "total_questions": tab.total_questions,
                "time_limit_minutes": tab.time_limit_minutes,
                "order": tab.order,
                "distributions": [],
                "mcqs": [],
            }
            for rule in tab.distribution_rules.all():
                tab_info["distributions"].append(
                    {
                        "subject": rule.subject,
                        "chapter": rule.chapter,
                        "sub_chapter": rule.sub_chapter,
                        "section": rule.section,
                        "difficulty": rule.difficulty,
                        "question_type": rule.question_type,
                        "question_count": rule.question_count,
                        "percentage": rule.percentage,
                    }
                )
            # Capture current MCQs (model-mcqid) for transparency after generate/regenerate
            questions = list(tab.questions.all().order_by("order", "id"))
            missing_ids = {q.mcq_id for q in questions if not q.mcq_model}

            # Best-effort resolve model for MCQs without stored model
            resolved_missing = {}
            if missing_ids:
                for model_name in _bank_model_choices():
                    model = _resolve_model(model_name)
                    if not model:
                        continue
                    for mid in model.objects.filter(id__in=missing_ids).values_list("id", flat=True):
                        if mid in resolved_missing:
                            resolved_missing[mid] = None  # ambiguous across models
                        else:
                            resolved_missing[mid] = model._meta.model_name

            tab_info["mcqs"] = [
                f"{(q.mcq_model or resolved_missing.get(q.mcq_id) or '').strip()}-{q.mcq_id}".lstrip('-')
                if (q.mcq_model or resolved_missing.get(q.mcq_id))
                else str(q.mcq_id)
                for q in questions
            ]
            tabs_payload.append(tab_info)
        return {"tabs": tabs_payload}

    @transaction.atomic
    def generate_mock(self, mock_test_id: int):
        mock = MockTest.objects.select_for_update().get(id=mock_test_id)
        # Remove only auto-generated questions; keep manual additions
        MockTestQuestion.objects.filter(mock_test=mock, added_manually=False).delete()
        for tab in mock.tabs.all():
            self._generate_tab(tab)
        mock.config_json = self._snapshot_config(mock)
        mock.save(update_fields=["config_json"])

    @transaction.atomic
    def regenerate_tab(self, mock_test_tab_id: int):
        tab = MockTestTab.objects.select_for_update().get(id=mock_test_tab_id)
        self._generate_tab(tab)
        mock = tab.mock_test
        mock.config_json = self._snapshot_config(mock)
        mock.save(update_fields=["config_json"])

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
            selected_ids.extend(picked)

        # Update tab totals
        tab.total_questions = MockTestQuestion.objects.filter(mock_test_tab=tab).count()
        tab.save(update_fields=["total_questions"])

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
