from collections import defaultdict

from django.apps import apps


def update_topic_performance(mock_test_attempt):
    """
    After a MockTestAttempt submission, aggregate QuestionAttempt data
    into TopicPerformance records per (subject, chapter, sub_chapter, section).
    """
    from students.models import TopicPerformance

    student = mock_test_attempt.student
    exam = mock_test_attempt.exam

    question_attempts = (
        mock_test_attempt.section_attempts
        .values_list("question_attempts", flat=False)
    )

    # Gather all QuestionAttempts across all SectionAttempts
    from students.models import QuestionAttempt

    qa_qs = QuestionAttempt.objects.filter(
        section_attempt__mock_test_attempt=mock_test_attempt,
    ).select_related("mock_test_question")

    # Group by topic key
    topic_data = defaultdict(lambda: {
        "total": 0,
        "correct": 0,
        "time_spent": [],
        "confusion_scores": [],
    })

    for qa in qa_qs:
        mtq = qa.mock_test_question
        mcq_model_name = mtq.mcq_model
        mcq_id = mtq.mcq_id

        try:
            McqModel = apps.get_model("bank", mcq_model_name)
            mcq_obj = McqModel.objects.get(pk=mcq_id)
        except (LookupError, McqModel.DoesNotExist):
            continue

        subject = getattr(mcq_obj, "subject_name", None) or mcq_model_name
        chapter = getattr(mcq_obj, "chapter", None) or ""
        sub_chapter = getattr(mcq_obj, "sub_chapter", None) or ""
        section = getattr(mcq_obj, "section", None) or ""

        if not chapter:
            continue

        key = (subject, chapter, sub_chapter, section)
        topic_data[key]["total"] += 1
        topic_data[key]["correct"] += int(qa.is_correct)
        topic_data[key]["time_spent"].append(qa.time_spent_seconds)
        topic_data[key]["confusion_scores"].append(qa.confusion_score)

    # Update or create TopicPerformance records
    for (subject, chapter, sub_chapter, section), data in topic_data.items():
        total = data["total"]
        correct = data["correct"]
        accuracy = (correct / total * 100) if total > 0 else 0
        avg_time = sum(data["time_spent"]) / len(data["time_spent"]) if data["time_spent"] else 0
        avg_confusion = (
            sum(data["confusion_scores"]) / len(data["confusion_scores"])
            if data["confusion_scores"]
            else 0
        )
        strength = (accuracy * 0.7) + ((1 - avg_confusion) * 0.3 * 100)
        weak = accuracy < 60 or avg_confusion > 0.6

        TopicPerformance.objects.update_or_create(
            student=student,
            exam=exam,
            subject=subject,
            chapter=chapter,
            sub_chapter=sub_chapter,
            section=section,
            defaults={
                "total_questions": total,
                "correct_questions": correct,
                "accuracy": accuracy,
                "avg_time_spent": avg_time,
                "avg_confusion_score": avg_confusion,
                "strength_score": strength,
                "weak_flag": weak,
            },
        )
