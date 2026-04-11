def recommend_next_action(student_profile, exam):
    from students.models import SubjectPerformance

    performances = SubjectPerformance.objects.filter(
        student=student_profile,
        exam=exam,
    )

    weakest = None
    lowest_score = 1.0

    for perf in performances:
        if perf.strength_score is None:
            continue

        if perf.strength_score < lowest_score:
            lowest_score = perf.strength_score
            weakest = perf.subject

    if weakest:
        return f"Recommended: Practice more questions in {weakest}"

    return "Continue current practice"
