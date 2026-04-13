# Comprehensive Ranking System

## Overview

A multi-level ranking system that computes and stores student rankings at 5 granularity levels after mock test submission. Rankings are persisted in the `StudentRanking` table and read directly by the leaderboard and cinematic race views — no on-the-fly computation or caching needed.

---

## Architecture

```
POST /api/submit-mocktest/
  │
  ├─ 1. Mark attempt: is_active=False, submitted_at=now()
  │
  ├─ 2. For each SectionAttempt:
  │     └─ finalize_section_attempt()          ← scoring.py
  │         ├─ calculate_confusion()            ← confusion.py
  │         ├─ set_review_outcome()             ← confusion.py
  │         ├─ update_section_confusion_summary()
  │         └─ compute_section_score()
  │
  ├─ 3. compute_mocktest_score()               ← scoring.py
  │
  ├─ 4. update_subject_performance()           ← performance.py
  │
  └─ 5. calculate_all_rankings()               ← ranking.py
        ├─ Level A: mocktest ranking
        ├─ Level B: tab ranking
        ├─ Level C: chapter / sub_chapter / section rankings
        └─ Level D: question stats
```

### File Responsibilities

| File | Purpose |
|------|---------|
| `scoring.py` | Computes scores (marks + confusion aggregation) |
| `ranking.py` | Computes & persists rankings + leaderboard reads |
| `performance.py` | Subject-level strength tracking |
| `confusion.py` | Per-question confusion calculation |

---

## Models

### StudentRanking (new)

| Field | Type | Description |
|-------|------|-------------|
| `mock_test_attempt` | FK → MockTestAttempt | The specific attempt being ranked |
| `student` | FK → StudentProfile | The student |
| `mock_test` | FK → MockTest | The mock test |
| `rank_type` | CharField (dropdown) | One of: `mocktest`, `tab`, `chapter`, `sub_chapter`, `section` |
| `rank_scope` | CharField | Identifies the scope (e.g. tab name, chapter name) |
| `score` | Float | Computed score for this scope |
| `total_questions` | Int | Questions attempted in this scope |
| `correct_questions` | Int | Correct answers in this scope |
| `accuracy` | Float | Percentage accuracy |
| `rank` | PositiveInt | Rank position (1 = best) |
| `total_participants` | PositiveInt | Total students ranked in this scope |
| `percentile` | Float | Percentile score |
| `created_at` | DateTime | Auto-set on creation |

**Unique constraint:** `(mock_test_attempt, rank_type, rank_scope)`

### MockTestAttempt (updated)

| Field | Type | Description |
|-------|------|-------------|
| `mocktest_attempt_count` | PositiveInt | Auto-incremented per student+mock_test pair on creation |

### MockTestQuestion (updated)

| Field | Type | Description |
|-------|------|-------------|
| `total_attempts` | PositiveInt | Total times this question was attempted across all students |
| `correct_attempts` | PositiveInt | Times answered correctly |

---

## Ranking Levels

### Level A — Mock Test Ranking
- **Scope:** Entire mock test
- **Score source:** `MockTestAttempt.total_score`
- **Rank scope key:** `mocktest_{mock_test_id}`

### Level B — Tab Ranking
- **Scope:** Per tab/section within the mock test
- **Score source:** `SectionAttempt.total_score`
- **Rank scope key:** `tab_{tab_name}`

### Level C-1 — Chapter Ranking
- **Scope:** Per chapter (resolved from MCQ bank)
- **Score source:** Sum of marks earned per question in that chapter
- **Rank scope key:** `chapter_{chapter_name}`

### Level C-2 — Sub-Chapter Ranking
- **Scope:** Per chapter > sub_chapter
- **Score source:** Sum of marks earned per question in that sub-chapter
- **Rank scope key:** `sub_chapter_{chapter > sub_chapter}`

### Level C-3 — Section Ranking
- **Scope:** Per chapter > sub_chapter > section
- **Score source:** Sum of marks earned per question in that section
- **Rank scope key:** `section_{chapter > sub_chapter > section}`

### Level D — Question Stats
- **Scope:** Per `MockTestQuestion`
- **Updates:** `total_attempts` and `correct_attempts` fields directly on the question

---

## Service: `ranking.py`

**Location:** `students/services/ranking.py`

### Entry Point

```python
from students.services.ranking import calculate_all_rankings

summary = calculate_all_rankings(mock_test_id)
# Returns: {"mocktest": 50, "tab": 150, "chapter": 200, "sub_chapter": 300, "section": 100, "questions_updated": 80}
```

### Behavior
1. Runs inside `@transaction.atomic`
2. Deletes all existing `StudentRanking` rows for the mock test
3. Recalculates all 5 levels (A → B → C1 → C2 → C3)
4. Updates question-level stats (Level D)
5. Returns summary dict with counts of created rankings

### Leaderboard Read

```python
from students.services.ranking import get_mocktest_leaderboard

qs = get_mocktest_leaderboard(mock_test_id)
# Returns StudentRanking queryset ordered by rank, with student__user prefetched
```

### Individual Functions

| Function | Level | Description |
|----------|-------|-------------|
| `calculate_all_rankings(mock_test_id)` | All | Orchestrates all levels below |
| `calculate_mocktest_rankings(mock_test_id)` | A | Overall ranking by total_score |
| `calculate_tab_rankings(mock_test_id)` | B | Per-tab ranking by section score |
| `calculate_chapter_rankings(mock_test_id)` | C-1 | Per-chapter ranking |
| `calculate_sub_chapter_rankings(mock_test_id)` | C-2 | Per-sub_chapter ranking |
| `calculate_section_rankings(mock_test_id)` | C-3 | Per-section ranking |
| `update_question_stats(mock_test_id)` | D | Update attempts/correct on MockTestQuestion |
| `get_mocktest_leaderboard(mock_test_id)` | Read | Query persisted mocktest-level rankings |

---

## MCQ Subject Resolution

Uses `MCQ_MODEL_SUBJECT_MAP` to derive subjects from mcq_model names:

| mcq_model | Subject |
|-----------|---------|
| `math` | Math |
| `reasoning` | Reasoning |
| `error` | English |
| `english` | English |

Topic fields (`chapter`, `sub_chapter`, `section`) are resolved dynamically via `apps.get_model("bank", mcq_model_name)`.

---

## API Endpoints

### `POST /api/submit-mocktest/`

Submits a mock test attempt and triggers the full scoring → ranking pipeline.

**Parameters:**
| Field | Type | Required |
|-------|------|----------|
| `mock_test_attempt_id` | int | Yes |

**Pipeline:**
1. Sets `is_active=False`, `submitted_at=now()`
2. Finalizes each section (confusion + scores)
3. Computes overall mock test score
4. Updates subject performance per tab
5. Calculates all rankings (5 levels + question stats)

**Response:**
```json
{
    "ok": true,
    "mock_test_attempt_id": 42,
    "total_score": 85.5,
    "ranking_summary": {"mocktest": 50, "tab": 150, "chapter": 200, ...}
}
```

### `GET /api/leaderboard/<mock_test_id>/`

Reads from persisted `StudentRanking` table (no on-the-fly computation).

### `GET /api/cinematic-race/<mock_test_id>/`

Reads from persisted `StudentRanking` table (no on-the-fly computation).

---

## Files Changed

| File | Change |
|------|--------|
| `students/models.py` | Added `mocktest_attempt_count` to MockTestAttempt, new `StudentRanking` model |
| `mocktest/models.py` | Added `total_attempts`, `correct_attempts` to MockTestQuestion |
| `students/services/ranking.py` | All ranking logic (merged from old ranking.py + ranking_engine.py) |
| `students/services/scoring.py` | Removed `invalidate_leaderboard_cache` dependency |
| `students/services/__init__.py` | Exports `calculate_all_rankings`, `get_mocktest_leaderboard` |
| `students/views.py` | New `submit_mocktest` endpoint; refactored `leaderboard` + `cinematic_race` to read from StudentRanking |
| `students/urls.py` | Added `submit-mocktest/` path |
| `students/admin.py` | Registered `StudentRanking` with admin site |
| `students/migrations/0011_*` | StudentRanking model + mocktest_attempt_count field |
| `mocktest/migrations/0008_*` | total_attempts + correct_attempts fields |

### Removed

| Item | Reason |
|------|--------|
| `ranking_engine.py` | Merged into `ranking.py` |
| `rank_mocktest_attempts()` | Replaced by `get_mocktest_leaderboard()` |
| `invalidate_leaderboard_cache()` | No cache layer — rankings are persisted |
| Cache layer in views | Leaderboard/cinematic now read directly from DB |

---

## Admin Panel

`StudentRanking` is available in Django admin with:
- **List display:** student, mock_test, rank_type, rank_scope, score, accuracy, rank, total_participants, percentile
- **Filters:** rank_type, mock_test
- **Search:** student username, rank_scope
