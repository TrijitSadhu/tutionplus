from django.db.models import Avg, Count, Q

from students.models import (
    MockTestAttempt,
    QuestionAttempt,
    SectionAttempt,
    SubjectPerformance,
)


def calculate_confusion(question_attempt: QuestionAttempt, question_avg_time: float = 60.0) -> float:
    base_confusion = 0.0

    if question_attempt.option_change_count >= 1:
        base_confusion += 0.4

    if question_attempt.time_spent_seconds > question_avg_time * 1.5:
        base_confusion += 0.3

    if question_attempt.was_ever_marked_for_review:
        base_confusion += 0.5

    if question_attempt.visit_count > 1:
        base_confusion += 0.2

    score = min(base_confusion, 1.0)
    question_attempt.confusion_score = score
    question_attempt.confusion_flag = score >= 0.5
    return score


def set_review_outcome(question_attempt: QuestionAttempt) -> str:
    """Assign review_outcome_type during submission. Does not save."""
    if question_attempt.was_ever_marked_for_review:
        if question_attempt.final_selected_option is None:
            outcome = "reviewed_skipped"
        elif question_attempt.is_correct:
            outcome = "reviewed_correct"
        else:
            outcome = "reviewed_wrong"
    else:
        outcome = "never_reviewed"

    question_attempt.review_outcome_type = outcome
    return outcome


def update_section_confusion_summary(section_attempt: SectionAttempt) -> tuple[int, float]:
    """Update SectionAttempt confusion aggregates at submission time."""
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


def update_subject_performance(
    *,
    student_profile,
    exam,
    subject: str,
    accuracy: float,
    speed_score: float,
    average_confusion_index: float,
    total_confused_questions: int,
    slide_factor: float = 0.5,
) -> SubjectPerformance:
    """Update SubjectPerformance with new metrics and apply downward slide on drops."""
    perf, _created = SubjectPerformance.objects.get_or_create(
        student=student_profile,
        exam=exam,
        subject=subject,
        defaults={
            "strength_score": 0,
            "previous_strength_score": 0,
            "mastery_streak": 0,
            "average_confusion_index": 0,
            "total_confused_questions": 0,
        },
    )

    perf.previous_strength_score = perf.strength_score

    computed_strength = (accuracy * 0.6) + (speed_score * 0.2) - (average_confusion_index * 0.2)

    # Downward slide: soften drops compared to previous_strength_score
    if computed_strength < perf.previous_strength_score:
        perf.strength_score = perf.previous_strength_score - (perf.previous_strength_score - computed_strength) * slide_factor
    else:
        perf.strength_score = computed_strength

    # Update mastery streak: increment on improvement/steady, reset on drop
    if perf.strength_score >= perf.previous_strength_score:
        perf.mastery_streak += 1
    else:
        perf.mastery_streak = 0

    perf.average_confusion_index = average_confusion_index
    perf.total_confused_questions = total_confused_questions

    perf.save(
        update_fields=[
            "strength_score",
            "previous_strength_score",
            "mastery_streak",
            "average_confusion_index",
            "total_confused_questions",
            "updated_at",
        ]
    )

    return perf