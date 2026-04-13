from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    selected_exams = models.ManyToManyField("mocktest.Exam", related_name="students", blank=True)
    active_exam = models.ForeignKey("mocktest.Exam", null=True, blank=True, on_delete=models.SET_NULL)
    is_paid = models.BooleanField(default=False, db_index=True)
    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", "id")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Profile for {self.user}"


class Payment(models.Model):
    STATUS_CHOICES = (
        ("initiated", "initiated"),
        ("success", "success"),
        ("failed", "failed"),
        ("refunded", "refunded"),
    )

    student = models.ForeignKey(StudentProfile, related_name="payments", on_delete=models.CASCADE, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=8, default="INR")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="initiated", db_index=True)
    provider = models.CharField(max_length=50, blank=True, default="")
    provider_reference = models.CharField(max_length=100, blank=True, default="", db_index=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    metadata = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "id")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Payment {self.transaction_id} ({self.status})"


class MockTestAttempt(models.Model):
    student = models.ForeignKey(StudentProfile, related_name="mock_test_attempts", on_delete=models.CASCADE)
    mock_test = models.ForeignKey("mocktest.MockTest", related_name="attempts", on_delete=models.CASCADE)
    exam = models.ForeignKey("mocktest.Exam", related_name="mock_test_attempts", on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True, db_index=True)
    started_at = models.DateTimeField(default=timezone.now)
    submitted_at = models.DateTimeField(null=True, blank=True)

    mocktest_attempt_count = models.PositiveIntegerField(default=1)

    total_score = models.FloatField(default=0, db_index=True)
    total_confused_questions = models.IntegerField(default=0)
    confusion_index = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", "id")
        indexes = [
            models.Index(fields=["student", "mock_test"]),
            models.Index(fields=["mock_test", "total_score"]),
            models.Index(fields=["is_active"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["student", "mock_test"],
                condition=Q(is_active=True),
                name="uniq_active_attempt_per_student_mock",
            )
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"MockTestAttempt {self.id} for {self.student}"

    def save(self, *args, **kwargs):
        if not self.exam_id and self.mock_test_id:
            exam_rel = self.mock_test.exam_relations.first()
            if exam_rel:
                self.exam = exam_rel
        if not self.pk:
            count = MockTestAttempt.objects.filter(
                student=self.student, mock_test=self.mock_test
            ).count()
            self.mocktest_attempt_count = count + 1
        super().save(*args, **kwargs)


class SectionAttempt(models.Model):
    mock_test_attempt = models.ForeignKey(
        MockTestAttempt,
        related_name="section_attempts",
        on_delete=models.CASCADE,
    )
    mock_test_tab = models.ForeignKey("mocktest.MockTestTab", related_name="section_attempts", on_delete=models.CASCADE)

    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_score = models.FloatField(default=0)
    total_confused_questions = models.IntegerField(default=0)
    average_confusion_score = models.FloatField(default=0)

    class Meta:
        ordering = ("-started_at", "id")
        indexes = [
            models.Index(fields=["mock_test_attempt", "mock_test_tab"]),
            models.Index(fields=["mock_test_attempt"]),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"SectionAttempt {self.id} for attempt {self.mock_test_attempt_id}"


class SubjectPerformance(models.Model):
    student = models.ForeignKey(StudentProfile, related_name="subject_performances", on_delete=models.CASCADE)
    exam = models.ForeignKey("mocktest.Exam", related_name="subject_performances", on_delete=models.CASCADE)
    subject = models.CharField(max_length=150, db_index=True)

    strength_score = models.FloatField(default=0)
    previous_strength_score = models.FloatField(default=0)
    mastery_streak = models.PositiveIntegerField(default=0)
    average_confusion_index = models.FloatField(default=0)
    total_confused_questions = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at", "id")
        unique_together = ("student", "exam", "subject")
        indexes = [
            models.Index(fields=["student", "exam", "subject"]),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"SubjectPerformance {self.subject} for {self.student}"


class QuestionAttempt(models.Model):
    REVIEW_OUTCOME_CHOICES = (
        ("never_reviewed", "never_reviewed"),
        ("reviewed_skipped", "reviewed_skipped"),
        ("reviewed_correct", "reviewed_correct"),
        ("reviewed_wrong", "reviewed_wrong"),
    )

    section_attempt = models.ForeignKey(SectionAttempt, related_name="question_attempts", on_delete=models.CASCADE, db_index=True)
    mock_test_question = models.ForeignKey("mocktest.MockTestQuestion", related_name="question_attempts", on_delete=models.CASCADE, db_index=True)

    selected_option = models.IntegerField(null=True, blank=True)
    final_selected_option = models.IntegerField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    time_spent_seconds = models.IntegerField(default=0)
    first_attempt_time_seconds = models.IntegerField(default=0)
    last_interaction_at = models.DateTimeField(null=True, blank=True)

    visit_count = models.IntegerField(default=0)
    option_change_count = models.IntegerField(default=0)
    mark_for_review_count = models.IntegerField(default=0)
    is_marked_for_review = models.BooleanField(default=False)
    was_ever_marked_for_review = models.BooleanField(default=False)

    confusion_flag = models.BooleanField(default=False)
    confusion_score = models.FloatField(default=0)

    review_outcome_type = models.CharField(max_length=32, choices=REVIEW_OUTCOME_CHOICES, default="never_reviewed")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("mock_test_question", "section_attempt", "id")
        unique_together = ("section_attempt", "mock_test_question")
        indexes = [
            models.Index(fields=["section_attempt"]),
            models.Index(fields=["mock_test_question"]),
            models.Index(fields=["section_attempt", "mock_test_question"]),
            models.Index(fields=["section_attempt"], condition=Q(confusion_flag=True), name="qa_confused_by_section_idx"),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"QA {self.mock_test_question_id} in {self.section_attempt_id}"


class TopicPerformance(models.Model):
    student = models.ForeignKey(StudentProfile, related_name="topic_performances", on_delete=models.CASCADE)
    exam = models.ForeignKey("mocktest.Exam", related_name="topic_performances", on_delete=models.CASCADE)
    subject = models.CharField(max_length=150, db_index=True)
    chapter = models.CharField(max_length=150, db_index=True)
    sub_chapter = models.CharField(max_length=150, blank=True, default="", db_index=True)
    section = models.CharField(max_length=150, blank=True, default="", db_index=True)

    total_questions = models.IntegerField(default=0)
    correct_questions = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)
    avg_time_spent = models.FloatField(default=0)
    avg_confusion_score = models.FloatField(default=0)
    strength_score = models.FloatField(default=0)
    weak_flag = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "exam", "subject", "chapter", "sub_chapter", "section")
        indexes = [
            models.Index(fields=["student", "exam"]),
            models.Index(fields=["student", "exam", "subject"]),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"TopicPerformance {self.subject}/{self.chapter} for {self.student}"


class StudentRanking(models.Model):
    RANK_TYPE_CHOICES = (
        ("mocktest", "Mock Test"),
        ("tab", "Tab / Section"),
        ("chapter", "Chapter"),
        ("sub_chapter", "Sub Chapter"),
        ("section", "Section"),
    )

    mock_test_attempt = models.ForeignKey(
        MockTestAttempt, related_name="rankings", on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        StudentProfile, related_name="rankings", on_delete=models.CASCADE
    )
    mock_test = models.ForeignKey(
        "mocktest.MockTest", related_name="rankings", on_delete=models.CASCADE
    )
    rank_type = models.CharField(max_length=20, choices=RANK_TYPE_CHOICES, db_index=True)
    rank_scope = models.CharField(
        max_length=255, db_index=True,
        help_text="Identifies the scope, e.g. tab name, chapter name, etc."
    )

    score = models.FloatField(default=0)
    total_questions = models.IntegerField(default=0)
    correct_questions = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)

    rank = models.PositiveIntegerField(default=0)
    total_participants = models.PositiveIntegerField(default=0)
    percentile = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("rank_type", "rank", "id")
        indexes = [
            models.Index(fields=["mock_test", "rank_type", "rank_scope"]),
            models.Index(fields=["student", "rank_type"]),
            models.Index(fields=["mock_test_attempt"]),
        ]
        unique_together = ("mock_test_attempt", "rank_type", "rank_scope")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Rank #{self.rank} ({self.rank_type}: {self.rank_scope}) for {self.student}"