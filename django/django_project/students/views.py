from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import logging
from django.db import transaction
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone

from students.models import QuestionAttempt, StudentProfile, SubjectPerformance
from students.services import rank_mocktest_attempts
from students.services.insights import generate_student_insights
from students.services.adaptive import recommend_next_action
from students.services.gamification import calculate_level
from students.services.topic_insights import generate_topic_insights
from students.models import MockTestAttempt, TopicPerformance

logger = logging.getLogger(__name__)


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

    insights = generate_student_insights(profile, active_exam)
    payload["insights"] = insights

    recommendation = recommend_next_action(profile, active_exam)
    payload["recommendation"] = recommendation

    level = calculate_level(profile, active_exam)
    payload["level"] = level

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


@login_required
def leaderboard(request, mock_test_id: int):
    profile = get_object_or_404(StudentProfile, user=request.user)
    cache_key = f"leaderboard:{mock_test_id}:student:{profile.id}"

    def _compute_payload():
        attempts_qs = MockTestAttempt.objects.filter(mock_test_id=mock_test_id, is_active=False, submitted_at__isnull=False)
        attempts_count = attempts_qs.count()
        if attempts_count > 200_000:
            logger.warning("High attempt volume for leaderboard mock_test_id=%s count=%s", mock_test_id, attempts_count)

        qs = (
            rank_mocktest_attempts(mock_test_id)
            .select_related("student__user")
            .only("id", "student__user__first_name", "student__user__last_name", "total_score", "student_id")
        )

        top_entries = []
        for entry in qs[:5]:
            user = entry.student.user
            name_parts = [user.first_name or "", user.last_name or ""]
            student_name = " ".join(p for p in name_parts if p).strip() or user.username
            top_entries.append(
                {
                    "rank": entry.rank,
                    "student_name": student_name,
                    "total_score": entry.total_score,
                }
            )

        topper_score = top_entries[0]["total_score"] if top_entries else None

        student_entry = qs.filter(student_id=profile.id).first()
        student_rank = student_entry.rank if student_entry else None
        student_score = student_entry.total_score if student_entry else None

        return {
            "mock_test_id": mock_test_id,
            "total_participants": attempts_count,
            "student_rank": student_rank,
            "student_score": student_score,
            "topper_score": topper_score,
            "leaderboard_top": top_entries,
        }

    payload = cache.get_or_set(cache_key, _compute_payload, timeout=60)
    return JsonResponse(payload)


@login_required
def cinematic_race(request, mock_test_id: int):
    profile = StudentProfile.objects.select_related("user").filter(user=request.user).first()
    if not profile:
        return JsonResponse({"error": "student profile not found"}, status=404)

    attempts_qs = MockTestAttempt.objects.filter(
        mock_test_id=mock_test_id, is_active=False, submitted_at__isnull=False
    )

    if not attempts_qs.filter(student_id=profile.id).exists():
        return JsonResponse({"error": "mock test not attemptednot attempts_qs"}, status=404)

    cache_key = f"cinematic_race:{mock_test_id}:{profile.id}"

    def _compute_payload():
        attempts_count = attempts_qs.count()
        ranking_qs = rank_mocktest_attempts(mock_test_id).select_related("student")

        student_entry = (
            ranking_qs.filter(student_id=profile.id).values("rank", "total_score").first()
        )
        if not student_entry:
            return {"error": "mock test not attempted"}

        top_three_entries = list(ranking_qs.values("rank", "total_score")[:3])
        topper_score = top_three_entries[0]["total_score"] if top_three_entries else None

        return {
            "mock_test_id": mock_test_id,
            "total_participants": attempts_count,
            "student_rank": student_entry["rank"],
            "student_score": student_entry["total_score"],
            "topper_score": topper_score,
            "top_three": top_three_entries,
        }

    payload = cache.get_or_set(cache_key, _compute_payload, timeout=60)

    if payload.get("error"):
        return JsonResponse(payload, status=404)

    return JsonResponse(payload)


@login_required
def topic_insights(request):
    profile = StudentProfile.objects.filter(user=request.user).first()
    if not profile:
        return JsonResponse({"error": "student profile not found"}, status=404)

    active_exam = profile.active_exam
    if not active_exam:
        return JsonResponse({"error": "active_exam not set"}, status=400)

    performances = TopicPerformance.objects.filter(
        student=profile, exam=active_exam,
    )

    # Try on-the-fly insights from QuestionAttempts if no TopicPerformance records
    live_topics = []
    if not performances.exists():
        live_topics = generate_topic_insights(profile, active_exam)

    weak_topics = []
    strong_topics = []
    confusion_scores = []

    for perf in performances:
        confusion_scores.append(perf.avg_confusion_score)
        strength = perf.strength_score / 100 if perf.strength_score > 1 else perf.strength_score

        entry = {
            "chapter": perf.chapter,
            "subject": perf.subject,
            "accuracy": round(perf.accuracy / 100, 2) if perf.accuracy > 1 else round(perf.accuracy, 2),
            "confusion": round(perf.avg_confusion_score, 2),
            "strength": round(strength, 2),
        }

        if perf.weak_flag:
            weak_topics.append(entry)
        elif perf.accuracy > 80:
            strong_topics.append(entry)

    weak_topics.sort(key=lambda t: (t["strength"], -t["confusion"]))

    avg_confusion = (
        sum(confusion_scores) / len(confusion_scores)
        if confusion_scores else 0
    )

    recommendation = "Continue current practice"
    if weak_topics:
        recommendation = "Focus on " + weak_topics[0]["chapter"]

    if not weak_topics and not strong_topics:
        # Use live topics if available, else demo data
        if live_topics:
            all_topics = live_topics
        else:
            all_topics = [
                {"subject": "Math", "chapter": "Time & Work", "accuracy": 0.3, "confusion": 0.6, "strength": 0.3},
                {"subject": "Math", "chapter": "Probability", "accuracy": 0.45, "confusion": 0.4, "strength": 0.4},
                {"subject": "English", "chapter": "Grammar", "accuracy": 0.85, "confusion": 0.1, "strength": 0.8},
            ]

        demo_weak = [t for t in all_topics if t["strength"] < 0.5]
        demo_strong = [t for t in all_topics if t["strength"] >= 0.7]
        demo_rec = "Practice weak topics" if demo_weak else "Continue current practice"

        return JsonResponse({
            "weak_topics": demo_weak,
            "strong_topics": demo_strong,
            "avg_confusion": 0.4,
            "recommendation": demo_rec,
        })

    return JsonResponse({
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "avg_confusion": round(avg_confusion, 3),
        "recommendation": recommendation,
    })


@login_required
def world_home(request):
    return render(request, "students/world/world_home.html")
