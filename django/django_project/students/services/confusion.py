from students.models import QuestionAttempt


def calculate_confusion(question_attempt: QuestionAttempt, question_avg_time: float = 60.0) -> float:
    """Compute confusion score using light signals; does not save."""
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
    """Assign review_outcome_type during submission; does not save."""
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
