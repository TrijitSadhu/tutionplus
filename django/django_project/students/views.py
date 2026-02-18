from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone

from students.models import QuestionAttempt, StudentProfile, SubjectPerformance


@login_required
def world_state(request):
    profile = get_object_or_404(
        StudentProfile.objects.select_related("active_exam__segment"), user=request.user
    )

    active_exam = profile.active_exam
    if not active_exam:
        return JsonResponse({"error": "active_exam not set"}, status=400)

    performances = list(
        SubjectPerformance.objects.filter(student=profile, exam=active_exam)
        .values(
            "subject",
            "strength_score",
            "previous_strength_score",
            "average_confusion_index",
            "total_confused_questions",
            "mastery_streak",
        )
        .order_by("subject")
    )

    subjects = [
        {
            "name": perf["subject"],
            "strength_score": perf["strength_score"],
            "previous_strength_score": perf["previous_strength_score"],
            "average_confusion_index": perf["average_confusion_index"],
            "total_confused_questions": perf["total_confused_questions"],
        }
        for perf in performances
    ]

    mastery_streak = max((perf["mastery_streak"] for perf in performances), default=0)

    payload = {
        "exam": active_exam.name,
        "theme": active_exam.segment.name if active_exam.segment else "",
        "subjects": subjects,
        "mastery_streak": mastery_streak,
    }

    return JsonResponse(payload)


@login_required
def question_update(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    try:
        question_attempt_id = int(request.POST.get("question_attempt_id"))
    except (TypeError, ValueError):
        return HttpResponseBadRequest("question_attempt_id required")

    selected_option_raw = request.POST.get("selected_option")
    selected_option = None
    if selected_option_raw not in (None, ""):
        try:
            selected_option = int(selected_option_raw)
        except ValueError:
            return HttpResponseBadRequest("selected_option must be int or blank")

    mark_for_review_raw = request.POST.get("is_marked_for_review")
    if mark_for_review_raw is None:
        mark_for_review = None
    else:
        mark_for_review = mark_for_review_raw.lower() in ("1", "true", "yes", "on")

    try:
        time_spent_delta = int(request.POST.get("time_spent_delta", 0))
    except ValueError:
        return HttpResponseBadRequest("time_spent_delta must be int")

    profile = get_object_or_404(StudentProfile, user=request.user)

    with transaction.atomic():
        qa = (
            QuestionAttempt.objects.select_for_update()
            .select_related("section_attempt__mock_test_attempt__student")
            .get(id=question_attempt_id)
        )

        if qa.section_attempt.mock_test_attempt.student_id != profile.id:
            return HttpResponseBadRequest("not permitted")

        if selected_option is not None:
            if qa.selected_option is not None and qa.selected_option != selected_option:
                qa.option_change_count += 1
            qa.selected_option = selected_option

        if mark_for_review is not None:
            if qa.is_marked_for_review != mark_for_review:
                qa.mark_for_review_count += 1
            qa.is_marked_for_review = mark_for_review
            qa.was_ever_marked_for_review = qa.was_ever_marked_for_review or mark_for_review

        if time_spent_delta and time_spent_delta > 0:
            qa.time_spent_seconds += time_spent_delta

        qa.last_interaction_at = timezone.now()
        qa.save(
            update_fields=
            [
                "selected_option",
                "option_change_count",
                "is_marked_for_review",
                "was_ever_marked_for_review",
                "mark_for_review_count",
                "time_spent_seconds",
                "last_interaction_at",
            ],
        )

    return JsonResponse({"ok": True})
