from __future__ import annotations

import logging
from collections import defaultdict

from django.apps import apps
from django.db import transaction
from django.db.models import Count, Q

from students.models import (
    MockTestAttempt,
    SectionAttempt,
    QuestionAttempt,
    StudentRanking,
)

logger = logging.getLogger(__name__)

MCQ_MODEL_SUBJECT_MAP = {
    "math": "Math",
    "reasoning": "Reasoning",
    "error": "English",
    "english": "English",
}


# ---------------------------------------------------------------------------
# Leaderboard helpers (read from persisted StudentRanking table)
# ---------------------------------------------------------------------------

def get_mocktest_leaderboard(mock_test_id):
    """Return StudentRanking queryset for mocktest-level, ordered by rank."""
    return (
        StudentRanking.objects.filter(
            mock_test_id=mock_test_id,
            rank_type="mocktest",
        )
        .select_related("student__user")
        .order_by("rank")
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _save_rankings(rows, mock_test_id, rank_type, rank_scope):
    """Sort rows by score desc and assign rank / percentile, then bulk-create."""
    rows.sort(key=lambda r: r["score"], reverse=True)
    total = len(rows)
    rankings = []
    for idx, row in enumerate(rows, start=1):
        percentile = ((total - idx) / total) * 100 if total > 0 else 0
        rankings.append(
            StudentRanking(
                mock_test_attempt_id=row["attempt_id"],
                student_id=row["student_id"],
                mock_test_id=mock_test_id,
                rank_type=rank_type,
                rank_scope=rank_scope,
                score=row["score"],
                total_questions=row["total_questions"],
                correct_questions=row["correct_questions"],
                accuracy=round(row["correct_questions"] / row["total_questions"] * 100, 2) if row["total_questions"] else 0,
                rank=idx,
                total_participants=total,
                percentile=round(percentile, 2),
            )
        )
    StudentRanking.objects.bulk_create(rankings)
    return len(rankings)


def _resolve_topic_field(mcq_model_name, mcq_id, field):
    """Resolve a topic field (chapter/sub_chapter/section) from the MCQ bank."""
    try:
        MCQModel = apps.get_model("bank", mcq_model_name)
        mcq = MCQModel.objects.filter(id=mcq_id).values_list(field, flat=True).first()
        return mcq or ""
    except Exception:
        return ""


def _build_topic_rankings(mock_test_id, rank_type, group_fields):
    """Generic builder for chapter / sub_chapter / section rankings."""
    from mocktest.models import MockTestQuestion

    attempts = MockTestAttempt.objects.filter(
        mock_test_id=mock_test_id,
        is_active=False,
        submitted_at__isnull=False,
    )

    mtq_qs = MockTestQuestion.objects.filter(mock_test_id=mock_test_id)
    mtq_topic_map = {}
    for mtq in mtq_qs:
        mcq_model = mtq.mcq_model or ""
        subject = MCQ_MODEL_SUBJECT_MAP.get(mcq_model.lower(), mcq_model)
        info = {"subject": subject}
        for field in ["chapter", "sub_chapter", "section"]:
            info[field] = _resolve_topic_field(mcq_model, mtq.mcq_id, field) if field in group_fields else ""
        mtq_topic_map[mtq.id] = info

    topic_groups = defaultdict(lambda: defaultdict(lambda: {
        "student_id": None, "score": 0.0, "total_questions": 0, "correct_questions": 0
    }))

    for att in attempts:
        qa_qs = QuestionAttempt.objects.filter(
            section_attempt__mock_test_attempt=att
        ).select_related("mock_test_question")

        for qa in qa_qs:
            mtq_id = qa.mock_test_question_id
            topic_info = mtq_topic_map.get(mtq_id)
            if not topic_info:
                continue

            key_parts = [topic_info.get(f, "") for f in group_fields]
            topic_key = " > ".join(p for p in key_parts if p) or "Unknown"

            entry = topic_groups[topic_key][att.id]
            entry["student_id"] = att.student_id
            entry["total_questions"] += 1
            if qa.is_correct:
                entry["correct_questions"] += 1
                entry["score"] += qa.mock_test_question.marks
            elif qa.selected_option is not None:
                entry["score"] -= qa.mock_test_question.negative_marks

    total_created = 0
    for topic_key, attempt_map in topic_groups.items():
        rows = []
        for attempt_id, data in attempt_map.items():
            rows.append({
                "attempt_id": attempt_id,
                "student_id": data["student_id"],
                "score": data["score"],
                "total_questions": data["total_questions"],
                "correct_questions": data["correct_questions"],
            })
        scope = f"{rank_type}_{topic_key}"
        total_created += _save_rankings(rows, mock_test_id, rank_type, scope)

    return total_created


# ---------------------------------------------------------------------------
# Per-level ranking calculators
# ---------------------------------------------------------------------------

def calculate_mocktest_rankings(mock_test_id):
    """Level A: Overall mock-test ranking by total_score."""
    attempts = MockTestAttempt.objects.filter(
        mock_test_id=mock_test_id,
        is_active=False,
        submitted_at__isnull=False,
    ).select_related("student")

    rows = []
    for att in attempts:
        total_q = att.section_attempts.aggregate(
            t=Count("question_attempts")
        )["t"] or 0
        correct_q = att.section_attempts.aggregate(
            c=Count("question_attempts", filter=Q(question_attempts__is_correct=True))
        )["c"] or 0
        rows.append({
            "attempt_id": att.id,
            "student_id": att.student_id,
            "score": att.total_score,
            "total_questions": total_q,
            "correct_questions": correct_q,
        })

    return _save_rankings(rows, mock_test_id, "mocktest", f"mocktest_{mock_test_id}")


def calculate_tab_rankings(mock_test_id):
    """Level B: Per-tab ranking by SectionAttempt.total_score."""
    from mocktest.models import MockTestTab

    tabs = MockTestTab.objects.filter(mock_test_id=mock_test_id).select_related("tab")
    total_created = 0

    for mtt in tabs:
        section_attempts = SectionAttempt.objects.filter(
            mock_test_tab=mtt,
            mock_test_attempt__mock_test_id=mock_test_id,
            mock_test_attempt__is_active=False,
            mock_test_attempt__submitted_at__isnull=False,
        ).select_related("mock_test_attempt")

        rows = []
        for sa in section_attempts:
            total_q = sa.question_attempts.count()
            correct_q = sa.question_attempts.filter(is_correct=True).count()
            rows.append({
                "attempt_id": sa.mock_test_attempt_id,
                "student_id": sa.mock_test_attempt.student_id,
                "score": sa.total_score,
                "total_questions": total_q,
                "correct_questions": correct_q,
            })

        scope = f"tab_{mtt.tab.name}"
        total_created += _save_rankings(rows, mock_test_id, "tab", scope)

    return total_created


def calculate_chapter_rankings(mock_test_id):
    """Level C-1: Per-chapter ranking."""
    return _build_topic_rankings(mock_test_id, "chapter", ["chapter"])


def calculate_sub_chapter_rankings(mock_test_id):
    """Level C-2: Per-sub_chapter ranking."""
    return _build_topic_rankings(mock_test_id, "sub_chapter", ["chapter", "sub_chapter"])


def calculate_section_rankings(mock_test_id):
    """Level C-3: Per-section ranking."""
    return _build_topic_rankings(mock_test_id, "section", ["chapter", "sub_chapter", "section"])


def update_question_stats(mock_test_id):
    """Level D: Update total_attempts and correct_attempts on MockTestQuestion."""
    from mocktest.models import MockTestQuestion

    questions = MockTestQuestion.objects.filter(mock_test_id=mock_test_id)
    updated = 0
    for mtq in questions:
        stats = QuestionAttempt.objects.filter(
            mock_test_question=mtq,
            section_attempt__mock_test_attempt__is_active=False,
            section_attempt__mock_test_attempt__submitted_at__isnull=False,
        ).aggregate(
            total=Count("id"),
            correct=Count("id", filter=Q(is_correct=True)),
        )
        mtq.total_attempts = stats["total"] or 0
        mtq.correct_attempts = stats["correct"] or 0
        mtq.save(update_fields=["total_attempts", "correct_attempts"])
        updated += 1
    return updated


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

@transaction.atomic
def calculate_all_rankings(mock_test_id):
    """Run all ranking levels for a given mock test.

    Deletes existing rankings for this mock test before recalculating.
    Returns a summary dict of created counts.
    """
    deleted, _ = StudentRanking.objects.filter(mock_test_id=mock_test_id).delete()
    logger.info("Deleted %d old rankings for mock_test_id=%s", deleted, mock_test_id)

    summary = {
        "mocktest": calculate_mocktest_rankings(mock_test_id),
        "tab": calculate_tab_rankings(mock_test_id),
        "chapter": calculate_chapter_rankings(mock_test_id),
        "sub_chapter": calculate_sub_chapter_rankings(mock_test_id),
        "section": calculate_section_rankings(mock_test_id),
        "questions_updated": update_question_stats(mock_test_id),
    }

    logger.info("Ranking complete for mock_test_id=%s: %s", mock_test_id, summary)
    return summary
