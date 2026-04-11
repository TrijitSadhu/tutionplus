def calculate_level(profile, exam):
    from students.models import SubjectPerformance

    performances = SubjectPerformance.objects.filter(
        student=profile,
        exam=exam,
    )

    if not performances.exists():
        return "Beginner"

    avg = sum(p.strength_score or 0 for p in performances) / performances.count()

    if avg < 0.3:
        return "Beginner"
    elif avg < 0.6:
        return "Intermediate"
    elif avg < 0.85:
        return "Advanced"
    else:
        return "Master"
