from django.db.models import Avg, Count, Q

from students.services.confusion import calculate_confusion, set_review_outcome
from students.models import MockTestAttempt, QuestionAttempt, SectionAttempt


def update_section_confusion_summary(section_attempt: SectionAttempt) -> tuple[int, float]:
    """Aggregate confusion for a section and persist lean fields."""
    metrics = section_attempt.question_attempts.aggregate(
        total_confused_questions=Count("id", filter=Q(confusion_flag=True)),
        average_confusion_score=Avg("confusion_score"),
    )
    section_attempt.total_confused_questions = metrics.get("total_confused_questions") or 0
    section_attempt.average_confusion_score = metrics.get("average_confusion_score") or 0.0
    section_attempt.save(update_fields=["total_confused_questions", "average_confusion_score"])
    return section_attempt.total_confused_questions, section_attempt.average_confusion_score


def update_mocktest_confusion_index(mocktest_attempt: MockTestAttempt, total_confused_questions: int | None = None) -> tuple[int, float]:
    """Compute and persist confusion_index for a mock test attempt."""
    if total_confused_questions is not None:
        mocktest_attempt.total_confused_questions = total_confused_questions

    total_questions = mocktest_attempt.mock_test.total_questions or 0
    confusion_index = 0.0
    if total_questions > 0:
        confusion_index = mocktest_attempt.total_confused_questions / total_questions

    mocktest_attempt.confusion_index = confusion_index
    mocktest_attempt.save(update_fields=["total_confused_questions", "confusion_index"])
    return mocktest_attempt.total_confused_questions, mocktest_attempt.confusion_index


def compute_section_score(section_attempt: SectionAttempt, questions: list[QuestionAttempt]) -> float:
    """Compute total score for a section in-memory from provided attempts."""
    total = 0.0
    mcq_lookup = {qa.mock_test_question_id: qa for qa in questions}
    for mtq in section_attempt.mock_test_tab.questions.all():
        qa = mcq_lookup.get(mtq.id)
        if not qa:
            continue
        total += mtq.marks if qa.is_correct else -mtq.negative_marks
    section_attempt.total_score = total
    section_attempt.save(update_fields=["total_score"])
    return total


def compute_mocktest_score(mocktest_attempt: MockTestAttempt) -> float:
    """Sum section scores into mock-level score; caller prefetches sections."""
    total = sum(section.total_score for section in mocktest_attempt.section_attempts.all())
    mocktest_attempt.total_score = total
    mocktest_attempt.save(update_fields=["total_score"])
    return total


def finalize_section_attempt(section_attempt: SectionAttempt, question_attempts_qs=None):
    """Bulk finalize a section attempt: compute confusion and review outcomes, aggregate, and score.

    The caller may pass a queryset already filtered by section_attempt; otherwise, it will be fetched with
    select_related("mock_test_question") to avoid N+1 queries. Uses bulk_update to avoid per-row saves.
    """

    qs = question_attempts_qs or QuestionAttempt.objects.select_related("mock_test_question").filter(
        section_attempt=section_attempt
    )
    attempts = list(qs)
    if not attempts:
        return 0.0

    for qa in attempts:
        calculate_confusion(qa)
        set_review_outcome(qa)

    QuestionAttempt.objects.bulk_update(
        attempts,
        ["confusion_score", "confusion_flag", "review_outcome_type"],
        batch_size=500,
    )

    update_section_confusion_summary(section_attempt)
    compute_section_score(section_attempt, attempts)
    return section_attempt.total_score
