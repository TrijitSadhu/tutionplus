def generate_student_insights(student_profile, exam):
    from students.models import SubjectPerformance

    performances = SubjectPerformance.objects.filter(
        student=student_profile,
        exam=exam,
    )

    insights = []

    for perf in performances:
        subject = perf.subject

        if perf.strength_score is None:
            continue

        if perf.strength_score < 0.4:
            insights.append(f"Weak area: {subject}. Focus practice.")

        if perf.average_confusion_index and perf.average_confusion_index > 0.5:
            insights.append(f"High confusion in {subject}. Revise concepts.")

        if perf.previous_strength_score is not None and perf.strength_score > perf.previous_strength_score:
            insights.append(f"Improving in {subject}. Keep going.")

        if perf.strength_score > 0.8:
            insights.append(f"Strong in {subject}. Maintain performance.")

    return insights
