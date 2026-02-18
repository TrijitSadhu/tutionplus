# MockTest App Documentation

## Purpose
Provides authoring, generation, and delivery of mock tests. Supports auto question distribution rules, manual curation, cached and resolved configs for runtime, exam-level aggregation, and admin tools to manage mocks and exam metadata.

## Models and Fields (mocktest/models.py)
- MockTest
  - exam (str, nullable, indexed): exam label; free-form.
  - title (str): display title.
  - mock_type (choice): mini | sectional | subject | full | practice | learning.
  - total_questions (int): cached count; recomputed when questions change.
  - total_marks (float): cached marks sum.
  - config_json (JSON): cached snapshot of tabs/questions for runtime.
  - is_active (bool, indexed): availability flag.
  - created_at (DateTime): creation timestamp.

- Tab
  - exam (str, nullable, indexed): exam label for grouping tabs.
  - name (str): human name (e.g., Physics, Quant).
  - order (int, indexed): display ordering.

- MockTestTab
  - mock_test (FK MockTest)
  - tab (FK Tab)
  - selection_mode (choice): auto (rules generate questions) | manual (questions added manually).
  - total_questions (int): desired count/cap per tab.
  - time_limit_minutes (int, nullable): optional per-tab timer.
  - order (int, indexed): ordering inside mock.
  - unique_together (mock_test, tab).

- MockDistributionRule
  - mock_test_tab (FK MockTestTab)
  - mcq_model (str, nullable, indexed): bank model to pull questions from.
  - subject / chapter / sub_chapter / section (str): filters for MCQ selection.
  - difficulty (str, indexed): difficulty filter.
  - question_type (str, indexed): e.g., single/multi-choice.
  - question_count (int, nullable): fixed count to pick.
  - percentage (float, nullable): percent of tab total to pick.
  - selected_mcq_ids (JSON list): last picked ids for tracking.
  - mcq_list (Text): comma string of picked ids (UI convenience).
  - clean(): requires either question_count or percentage.

- MockTestQuestion
  - mock_test (FK MockTest)
  - mock_test_tab (FK MockTestTab)
  - mcq_model (str, nullable, indexed): MCQ model name.
  - mcq_id (int, indexed): MCQ id.
  - order (int, indexed): position in tab.
  - marks (float): positive marks.
  - negative_marks (float): penalty.
  - added_manually (bool, indexed): distinguishes manual additions from auto-generated.
  - unique_together (mock_test, mcq_model, mcq_id).

- Segment
  - name (str, unique, indexed): exam segment/category.
  - created_at (DateTime): audit.

- Exam
  - segment (FK Segment)
  - name (str, indexed)
  - year (int, indexed)
  - exam_date (Date, nullable)
  - state (choice): state/region.
  - mock_tests (M2M MockTest): mocks under this exam.
  - created_at (DateTime)
  - unique_together (segment, name, year, state).

- ExamSummary
  - exam (OneToOne Exam)
  - total_mock_tests, total_questions, total_marks (ints/floats): aggregates.
  - total_tabs, total_distribution_rules, total_question_objects (ints): structure counts.
  - full_mocks_count, sectional_mocks_count, mini_mocks_count, practice_mocks_count, learning_mocks_count (ints): mock_type counts.
  - active_mocks_count, inactive_mocks_count (ints): status counts.
  - earliest_mock_created, latest_mock_created (DateTime): range.
  - updated_at (auto): last summary update.

## Services (mocktest/services/mock_generator.py)
- MockTestGeneratorService
  - generate_mock(mock_test_id): rebuilds auto tabs; deletes non-manual questions, picks questions per rules, refreshes config_json and totals.
  - regenerate_tab(mock_test_tab_id): rebuilds a single tab (auto mode only) and refreshes config_json.
  - update_config_from_existing(mock_test_id): snapshot config_json without changing questions.
  - validate_distribution(mock_test_id) -> list[str]: checks rule coverage per tab (percentage totals, counts vs capacity, missing counts) and returns issues.
  - Internal helpers:
    - _snapshot_config(mock): builds cached config payload including mcq strings and mcq_details (marks/order), resolving basic MCQ metadata when possible.
    - _recalc_mock_totals(mock): recomputes total_questions and total_marks from MockTestQuestion rows.
    - _filtered_queryset(rule): builds queryset for bank MCQs matching rule filters.
    - _pick_mcq_ids(qs, needed, excluded_ids): random sampling with optional exclusion.

- resolve_config_mcqs(config: dict) -> dict
  - Takes cached/live config, bulk-fetches MCQ records by model and id/new_id, and returns config with tabs enriched by mcq_records (question text, options, answers, difficulty, subject, etc.) while preserving order.

- _parse_mcq_string(raw: str) -> (model, id|None, new_id|None)
  - Splits tokens like model$$$id$$$new_id for resolver use.

## Views / Endpoints (mocktest/views.py, mocktest/urls.py)
- GET /api/mocktests/<id>/config/ (mocktest_config_cached)
  - Returns mock.config_json; if empty, snapshots live config first.

- GET /api/mocktests/<id>/config/live/ (mocktest_config_live)
  - Regenerates a fresh snapshot (no DB changes) and returns it.

- GET /api/mocktests/<id>/config/resolved/ (mocktest_config_resolved)
  - Returns cached/live config with MCQ details resolved via resolve_config_mcqs.

- GET /mocktests/<id>/exam/ (mocktest_runner)
  - Renders template shell; client fetches data from resolved API.

- GET/POST exam_update_view (admin-ish page for Exam)
  - Uses ExamForm; updates Exam data and mock_tests selection; renders mocktest/exam_update.html.

## Admin (mocktest/admin.py)
Registered on bank.admin.admin_site with extensive tooling:
- MockTestAdmin: inlines tabs/questions; actions to generate/regenerate mocks, validate distribution, and update config_json. Custom pages: modify_view (summary with fetched MCQ metadata), distribute_view (manage rules), and many AJAX endpoints for MCQ CRUD, reordering, replacing, rule add/delete, regenerate mock/tab, and search/filter helpers (models/subjects/chapters/sections, MCQ search).
- TabAdmin: basic listing and search.
- MockTestTabAdmin: tab listing/filtering.
- MockDistributionRuleAdmin: rule listing, filters, search.
- MockTestQuestionAdmin: question listing, manual flag filter, custom change template.
- SegmentAdmin, ExamAdmin (with select_mocktests custom view, Request-bound ExamForm, summary display), ExamSummaryAdmin (recalc on save), Exam.mock_tests through admin for M2M visibility.

## Forms (mocktest/forms.py)
- ExamForm
  - Base fields: segment, name, year, exam_date, state, mock_tests.
  - Extra filter fields via GET params: title, exam, mock_type, is_active, date_from, date_to, min/max questions, min/max marks.
  - Populates mock_tests queryset based on filters while preserving already-selected mocks; hides default help text.

## Signals (mocktest/signals.py)
- recalc_exam_summary(exam): recomputes ExamSummary aggregates (counts, marks, tabs, rules, questions, status/mode breakdowns, earliest/latest dates). Clears metrics when no mocks.
- update_exam_summary_on_mock_change: m2m_changed hook on Exam.mock_tests; triggers recalc on add/remove/clear.

## Typical Data Flow
1) Authoring: Admin creates MockTest with tabs and rules (auto) or manual questions.
2) Generation: Admin actions or AJAX endpoints call MockTestGeneratorService.generate_mock/regenerate_tab to populate MockTestQuestion rows and refresh config_json and totals.
3) Caching: config_json stores a snapshot (mcq strings + details) for fast API responses.
4) Delivery: Clients call /api/mocktests/<id>/config/ (cached) or /config/resolved/ (with MCQ records) to drive exam UI; /config/live/ can bypass stale cache.
5) Exams: Exams group MockTests; signals keep ExamSummary in sync when M2M changes; admin views/forms let staff filter/select mocks per exam.

## Usage Examples
- Generate an entire mock after setting rules:
```python
service = MockTestGeneratorService()
service.generate_mock(mock_test_id=42)
```

- Regenerate only one tab:
```python
service = MockTestGeneratorService()
service.regenerate_tab(mock_test_tab_id=7)
```

- Refresh config_json from current questions (no repick):
```python
service = MockTestGeneratorService()
service.update_config_from_existing(mock_test_id=42)
```

- Validate distribution for a mock and report issues:
```python
issues = MockTestGeneratorService().validate_distribution(mock_test_id=42)
if issues:
    for msg in issues:
        print("warn:", msg)
```

- Resolve MCQ details for a cached config (e.g., in a view):
```python
from mocktest.services.mock_generator import resolve_config_mcqs
payload = resolve_config_mcqs(mock.config_json)
```

- Call cached config API:
```
GET /api/mocktests/42/config/
```

- Call resolved config API (includes MCQ content):
```
GET /api/mocktests/42/config/resolved/
```

## Notes
- MockDistributionRule.clean enforces at least one of question_count or percentage.
- generation respects selection_mode: auto tabs regenerate; manual tabs are untouched.
- MockTestQuestion uniqueness prevents duplicates of the same MCQ/model within a mock.
- ExamSummary is maintained automatically via signals on the Exam.mock_tests relation.
- Cached config uses mcq strings "model$$$id" or "model$$$id$$$new_id"; resolver prefers new_id when present.
