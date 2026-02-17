from django.db.models import Q, Min, Max, Sum, Count
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from mocktest.models import (
    Exam,
    ExamSummary,
    MockDistributionRule,
    MockTestQuestion,
    MockTestTab,
)


def recalc_exam_summary(exam):
    mock_qs = exam.mock_tests.all()
    summary, _ = ExamSummary.objects.get_or_create(exam=exam)

    if not mock_qs.exists():
        summary.total_mock_tests = 0
        summary.total_questions = 0
        summary.total_marks = 0
        summary.total_tabs = 0
        summary.total_distribution_rules = 0
        summary.total_question_objects = 0
        summary.full_mocks_count = 0
        summary.sectional_mocks_count = 0
        summary.mini_mocks_count = 0
        summary.practice_mocks_count = 0
        summary.learning_mocks_count = 0
        summary.active_mocks_count = 0
        summary.inactive_mocks_count = 0
        summary.earliest_mock_created = None
        summary.latest_mock_created = None
        summary.save(
            update_fields=[
                "total_mock_tests",
                "total_questions",
                "total_marks",
                "total_tabs",
                "total_distribution_rules",
                "total_question_objects",
                "full_mocks_count",
                "sectional_mocks_count",
                "mini_mocks_count",
                "practice_mocks_count",
                "learning_mocks_count",
                "active_mocks_count",
                "inactive_mocks_count",
                "earliest_mock_created",
                "latest_mock_created",
                "updated_at",
            ]
        )
        return summary

    aggregates = mock_qs.aggregate(
        total_mock_tests=Count("id", distinct=True),
        total_questions=Sum("total_questions"),
        total_marks=Sum("total_marks"),
        earliest=Min("created_at"),
        latest=Max("created_at"),
        active_mocks=Count("id", filter=Q(is_active=True), distinct=True),
        inactive_mocks=Count("id", filter=Q(is_active=False), distinct=True),
        full_mocks=Count("id", filter=Q(mock_type="full"), distinct=True),
        sectional_mocks=Count("id", filter=Q(mock_type="sectional"), distinct=True),
        mini_mocks=Count("id", filter=Q(mock_type="mini"), distinct=True),
        practice_mocks=Count("id", filter=Q(mock_type="practice"), distinct=True),
        learning_mocks=Count("id", filter=Q(mock_type="learning"), distinct=True),
    )

    summary.total_mock_tests = aggregates.get("total_mock_tests") or 0
    summary.total_questions = aggregates.get("total_questions") or 0
    summary.total_marks = aggregates.get("total_marks") or 0
    summary.earliest_mock_created = aggregates.get("earliest")
    summary.latest_mock_created = aggregates.get("latest")

    summary.full_mocks_count = aggregates.get("full_mocks") or 0
    summary.sectional_mocks_count = aggregates.get("sectional_mocks") or 0
    summary.mini_mocks_count = aggregates.get("mini_mocks") or 0
    summary.practice_mocks_count = aggregates.get("practice_mocks") or 0
    summary.learning_mocks_count = aggregates.get("learning_mocks") or 0
    summary.active_mocks_count = aggregates.get("active_mocks") or 0
    summary.inactive_mocks_count = aggregates.get("inactive_mocks") or 0

    summary.total_tabs = MockTestTab.objects.filter(mock_test__in=mock_qs).count()
    summary.total_distribution_rules = MockDistributionRule.objects.filter(mock_test_tab__mock_test__in=mock_qs).count()
    summary.total_question_objects = MockTestQuestion.objects.filter(mock_test__in=mock_qs).count()

    summary.save(
        update_fields=[
            "total_mock_tests",
            "total_questions",
            "total_marks",
            "total_tabs",
            "total_distribution_rules",
            "total_question_objects",
            "full_mocks_count",
            "sectional_mocks_count",
            "mini_mocks_count",
            "practice_mocks_count",
            "learning_mocks_count",
            "active_mocks_count",
            "inactive_mocks_count",
            "earliest_mock_created",
            "latest_mock_created",
            "updated_at",
        ]
    )
    return summary


@receiver(m2m_changed, sender=Exam.mock_tests.through)
def update_exam_summary_on_mock_change(sender, instance, action, **kwargs):
    if action not in {"post_add", "post_remove", "post_clear"}:
        return
    recalc_exam_summary(instance)
