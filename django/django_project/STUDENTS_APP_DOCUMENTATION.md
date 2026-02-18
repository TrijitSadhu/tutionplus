# Students App Documentation

## Purpose
Tracks a learner's state across mock tests, sections, subjects, and individual question interactions. Provides analytics (confusion, strength, mastery streaks) and API endpoints to surface world state and persist question-level interactions.

## Models and Fields
- StudentProfile
  - user (OneToOne): link to auth user; primary identity for student data.
  - selected_exams (M2M Exam): exams the student follows.
  - active_exam (FK Exam, nullable): drives world_state API.
  - is_paid (bool): subscription flag.
  - subscription_start/end (DateTime): subscription window.
  - created_at (auto): audit.

- Payment
  - student (FK StudentProfile, indexed)
  - amount (Decimal), currency (char)
  - status (enum): initiated | success | failed | refunded (indexed)
  - provider, provider_reference (indexed), transaction_id (unique)
  - metadata (short text), created_at/updated_at, paid_at

- MockTestAttempt
  - student (FK StudentProfile), mock_test (FK MockTest), exam (FK Exam)
  - is_active (bool, indexed) with partial unique constraint per (student, mock_test) to block multiple active attempts
  - started_at, submitted_at
  - total_score (float, indexed), total_confused_questions (int), confusion_index (float)
  - Indexes: (student, mock_test), (mock_test, total_score)

 SectionAttempt
  - mock_test_attempt (FK MockTestAttempt, required; enforced non-null via migration backfill)
  - mock_test_tab (FK MockTestTab)
  - started_at / completed_at
  - total_score (float), total_confused_questions (int), average_confusion_score (float)
  - Indexes: (mock_test_attempt, mock_test_tab) and (mock_test_attempt)

- SubjectPerformance
  - student (FK StudentProfile)
  - exam (FK Exam)
  - subject (str, db_index)
  - strength_score, previous_strength_score, mastery_streak
  - average_confusion_index, total_confused_questions
  - unique_together (student, exam, subject) with index

 - QuestionAttempt
  - section_attempt (FK SectionAttempt, indexed)
  - mock_test_question (FK MockTestQuestion, indexed)
  - selected_option, final_selected_option, is_correct
  - time_spent_seconds, first_attempt_time_seconds, last_interaction_at
  - visit_count, option_change_count, mark_for_review_count, is_marked_for_review, was_ever_marked_for_review
  - confusion_flag, confusion_score
  - review_outcome_type: never_reviewed | reviewed_skipped | reviewed_correct | reviewed_wrong
  - created_at (auto)
  - Indexes: section_attempt, mock_test_question, composite (section_attempt, mock_test_question), and partial index on section_attempt where confusion_flag=TRUE; unique_together on (section_attempt, mock_test_question)

## Services (students/services/*)
- confusion.py
  - calculate_confusion(question_attempt, question_avg_time=60.0): weighted signals (option change, long time, review flag, multiple visits) capped at 1.0; sets confusion_flag at >=0.5.
  - set_review_outcome(question_attempt): sets review_outcome_type from review flag, correctness, final selection.

- scoring.py
  - update_section_confusion_summary(section_attempt): aggregates confusion metrics; saves section.
  - update_mocktest_confusion_index(mocktest_attempt, total_confused_questions=None): persists confusion_index against mock total_questions.
  - compute_section_score(section_attempt, questions): sum marks/negative using provided QuestionAttempt list and tab questions; saves total_score.
  - compute_mocktest_score(mocktest_attempt): sums section total_score into attempt total_score.
  - finalize_section_attempt(section_attempt, question_attempts_qs=None): select_related fetch, compute confusion/review, bulk_update QAs, aggregate confusion, and compute section score without per-row saves.

- performance.py
  - update_subject_performance(...): clamps accuracy/speed/confusion to [0,1], applies strength formula (accuracy*0.6 + speed*0.2 - confusion*0.2) with downward slide factor, clamps strength to [0,1], updates mastery_streak and confusion aggregates.

- ranking.py
  - rank_mocktest_attempts(mock_test_id): ranks only submitted attempts (is_active=False and submitted_at set) using PostgreSQL RANK() over total_score DESC NULLS LAST.

## Views / Endpoints (students/views.py, students/urls.py)
- GET /api/world-state/ (world_state)
  - Auth: login required.
  - Uses StudentProfile.active_exam (must exist) and SubjectPerformance records.
  - Response: { exam, theme, subjects: [{name, strength_score, previous_strength_score, average_confusion_index, total_confused_questions}], mastery_streak (max across subjects) }.

- POST /api/question-update/ (question_update)
  - Auth: login required.
  - Body (form-encoded): question_attempt_id (int, required); selected_option (int or blank); is_marked_for_review (bool-like); time_spent_delta (int seconds, optional).
  - Behavior: locks QuestionAttempt, ensures ownership, increments option_change_count on change, toggles mark_for_review with mark_for_review_count, accumulates time_spent_seconds, sets was_ever_marked_for_review when flagged, updates last_interaction_at, saves, returns {"ok": true}. Returns 400 on invalid input or unauthorized access.

## Admin (students/admin.py)
Registered on bank.admin.admin_site:
- StudentProfile: list user/active_exam/is_paid.
- SectionAttempt: list student/mock_test/tab/confusion aggregates.
- QuestionAttempt: list selection/change/review/confusion fields; filters for confusion_flag and is_marked_for_review.
- MockTestAttempt: list confusion_index totals.
- SubjectPerformance: list strength, mastery_streak, confusion aggregates; filters by exam/subject.

## Typical Data Flow
1) Attempt creation: create MockTestAttempt (enforced single active per mock), then SectionAttempt rows and QuestionAttempt rows per tab.
2) During play: POST /api/question-update/ uses select_for_update to update QuestionAttempt counters and timing.
3) Submission: caller sets final_selected_option/is_correct, runs calculate_confusion + set_review_outcome, saves QA rows.
4) Section aggregation: update_section_confusion_summary and compute_section_score persist SectionAttempt aggregates.
5) Mock aggregation: compute_mocktest_score and update_mocktest_confusion_index persist attempt totals.
6) Subject update: update_subject_performance ingests accuracy/speed/confusion to refresh SubjectPerformance.
7) Ranking: rank_mocktest_attempts uses RANK() window over total_score; avoid Python loops.
8) World display: GET /api/world-state/ reads only SubjectPerformance for active_exam; no heavy joins.

## Usage Examples
- Compute confusion and review outcome before saving:
```python
qa = QuestionAttempt.objects.get(id=qa_id)
calculate_confusion(qa)
set_review_outcome(qa)
qa.save(update_fields=[
    "confusion_score",
    "confusion_flag",
    "review_outcome_type",
    "final_selected_option",
    "is_correct",
])
```

- After a section submission:
```python
section = SectionAttempt.objects.get(id=section_id)
update_section_confusion_summary(section)
mock_attempt = MockTestAttempt.objects.get(student=section.student, mock_test=section.mock_test)
update_mocktest_confusion_index(mock_attempt)
```

- Update subject performance when grading a mock:
```python
update_subject_performance(
    student_profile=section.student,
    exam=section.mock_test.exam_relations.first(),
    subject="Physics",
    accuracy=0.78,
    speed_score=0.65,
    average_confusion_index=mock_attempt.confusion_index,
    total_confused_questions=mock_attempt.total_confused_questions,
)
```

- Calling question-update API (form POST):
```
POST /api/question-update/
question_attempt_id=123
selected_option=2
is_marked_for_review=true
time_spent_delta=15
```
Response: {"ok": true}

- Calling world-state API:
```
GET /api/world-state/
```
Response example:
```json
{
  "exam": "JEE Main 2026",
  "theme": "Engineering",
  "subjects": [
    {
      "name": "Physics",
      "strength_score": 0.72,
      "previous_strength_score": 0.68,
      "average_confusion_index": 0.18,
      "total_confused_questions": 5
    }
  ],
  "mastery_streak": 3
}
```

## Notes
- Confusion thresholds: confusion_flag triggers at score >= 0.5.
- Strength sliding: slide_factor softens drops to avoid sharp declines; set slide_factor to 1.0 to disable smoothing.
- Ensure StudentProfile.active_exam is set; world_state returns 400 otherwise.
- QuestionAttempt uniqueness: one record per (section_attempt, mock_test_question); reuse same record for updates.
