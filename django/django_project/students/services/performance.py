from students.models import SubjectPerformance


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


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
    """Update SubjectPerformance with new metrics and apply downward slide on drops.

    Inputs are normalized to [0,1] before computing strength; strength is clamped to [0,1].
    """
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

    acc = _clamp(accuracy)
    speed = _clamp(speed_score)
    confusion = _clamp(average_confusion_index)

    computed_strength = _clamp((acc * 0.6) + (speed * 0.2) - (confusion * 0.2))

    if computed_strength < perf.previous_strength_score:
        perf.strength_score = perf.previous_strength_score - (perf.previous_strength_score - computed_strength) * slide_factor
    else:
        perf.strength_score = computed_strength

    perf.strength_score = _clamp(perf.strength_score)

    if perf.strength_score >= perf.previous_strength_score:
        perf.mastery_streak += 1
    else:
        perf.mastery_streak = 0

    perf.average_confusion_index = confusion
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
