from collections import defaultdict

from django.apps import apps

# Map bank model names to display subjects
MCQ_MODEL_SUBJECT_MAP = {
    "math": "Math",
    "reasoning": "Reasoning",
    "error": "English",
    "english": "English",
}


def generate_topic_insights(student, exam):
    """
    Generate topic-level insights on-the-fly from QuestionAttempts
    by resolving MCQ models dynamically via mcq_model + mcq_id.
    Returns a list of structured topic dicts with subject, chapter,
    accuracy, confusion, and strength.
    """
    from students.models import QuestionAttempt

    qa_qs = QuestionAttempt.objects.filter(
        section_attempt__mock_test_attempt__student=student,
        section_attempt__mock_test_attempt__exam=exam,
        section_attempt__mock_test_attempt__is_active=False,
    ).select_related("mock_test_question")

    # Group by (subject, chapter)
    topic_data = defaultdict(lambda: {
        "total": 0,
        "correct": 0,
        "confused": 0,
        "time_spent": 0,
    })

    for qa in qa_qs:
        mtq = qa.mock_test_question
        mcq_model_name = mtq.mcq_model
        mcq_id = mtq.mcq_id

        if not mcq_model_name:
            continue

        try:
            McqModel = apps.get_model("bank", mcq_model_name)
            question = McqModel.objects.get(pk=mcq_id)
        except (LookupError, Exception):
            continue

        if not question:
            continue

        # Derive subject from model name
        subject = MCQ_MODEL_SUBJECT_MAP.get(mcq_model_name.lower(), "General")
        chapter = getattr(question, "chapter", None) or "Unknown"

        key = (subject, chapter)
        topic_data[key]["total"] += 1
        topic_data[key]["correct"] += int(qa.is_correct)
        topic_data[key]["confused"] += int(qa.confusion_flag)
        topic_data[key]["time_spent"] += qa.time_spent_seconds

    if not topic_data:
        return []

    topics_output = []

    for (subject, chapter), data in topic_data.items():
        total = data["total"]
        if total == 0:
            continue

        accuracy = data["correct"] / total
        confusion_rate = data["confused"] / total
        strength = (accuracy * 0.7) + ((1 - confusion_rate) * 0.3)

        topics_output.append({
            "subject": subject,
            "chapter": chapter,
            "accuracy": round(accuracy, 2),
            "confusion": round(confusion_rate, 2),
            "strength": round(strength, 2),
        })

    return topics_output
