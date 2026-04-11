def generate_study_plan(student, exam):
    from students.models import TopicPerformance

    performances = TopicPerformance.objects.filter(
        student=student,
        exam=exam,
    )

    weak_topics = []
    medium_topics = []
    strong_topics = []

    for perf in performances:
        topic = {
            "subject": perf.subject,
            "chapter": perf.chapter,
            "sub_chapter": perf.sub_chapter,
            "section": perf.section,
            "accuracy": perf.accuracy,
            "avg_confusion_score": perf.avg_confusion_score,
            "strength_score": perf.strength_score,
        }

        if perf.weak_flag:
            weak_topics.append(topic)
        elif perf.accuracy <= 80:
            medium_topics.append(topic)
        else:
            strong_topics.append(topic)

    weak_topics.sort(key=lambda t: (t["accuracy"], -t["avg_confusion_score"]))
    medium_topics.sort(key=lambda t: t["accuracy"])

    return {
        "focus": weak_topics[:3],
        "revise": medium_topics[:3],
        "skip": strong_topics,
        "message": "Focus on improving weak areas first",
    }
