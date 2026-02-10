from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


class MockTest(models.Model):
	MOCK_TYPE_CHOICES = (
		("mini", "mini"),
		("sectional", "sectional"),
		("subject", "subject"),
		("full", "full"),
		("practice", "practice"),
		("learning", "learning"),
	)

	exam = models.CharField(max_length=100, blank=True, null=True, db_index=True)
	title = models.CharField(max_length=255)
	mock_type = models.CharField(max_length=20, choices=MOCK_TYPE_CHOICES, default="full", db_index=True)
	total_questions = models.PositiveIntegerField(default=0)
	total_marks = models.FloatField(default=0)
	config_json = JSONField(default=dict, blank=True)
	is_active = models.BooleanField(default=True, db_index=True)
	created_at = models.DateTimeField(default=timezone.now, db_index=True)

	class Meta:
		ordering = ("-created_at", "-id")

	def __str__(self) -> str:  # pragma: no cover - trivial
		return f"{self.title} ({self.mock_type})"


class Tab(models.Model):
	exam = models.CharField(max_length=100, blank=True, null=True, db_index=True)
	name = models.CharField(max_length=150)
	order = models.PositiveIntegerField(default=0, db_index=True)

	class Meta:
		ordering = ("order", "id")

	def __str__(self) -> str:  # pragma: no cover - trivial
		return self.name


class MockTestTab(models.Model):
	SELECTION_MODE_CHOICES = (
		("auto", "auto"),
		("manual", "manual"),
	)

	mock_test = models.ForeignKey(MockTest, related_name="tabs", on_delete=models.CASCADE)
	tab = models.ForeignKey(Tab, related_name="instances", on_delete=models.PROTECT)
	selection_mode = models.CharField(max_length=10, choices=SELECTION_MODE_CHOICES, default="auto", db_index=True)
	total_questions = models.PositiveIntegerField(default=0)
	time_limit_minutes = models.PositiveIntegerField(blank=True, null=True)
	order = models.PositiveIntegerField(default=0, db_index=True)

	class Meta:
		ordering = ("order", "id")
		unique_together = ("mock_test", "tab")

	def __str__(self) -> str:  # pragma: no cover - trivial
		return f"{self.mock_test} - {self.tab.name}"


class MockDistributionRule(models.Model):
	mock_test_tab = models.ForeignKey(MockTestTab, related_name="distribution_rules", on_delete=models.CASCADE)
	mcq_model = models.CharField(max_length=100, blank=True, null=True, db_index=True)
	subject = models.CharField(max_length=150, db_index=True)
	chapter = models.CharField(max_length=150, blank=True, null=True, db_index=True)
	sub_chapter = models.CharField(max_length=150, blank=True, null=True, db_index=True)
	section = models.CharField(max_length=150, blank=True, null=True, db_index=True)
	difficulty = models.CharField(max_length=50, blank=True, null=True, db_index=True)
	question_type = models.CharField(max_length=20, blank=True, null=True, db_index=True)
	question_count = models.PositiveIntegerField(blank=True, null=True)
	percentage = models.FloatField(blank=True, null=True)
	selected_mcq_ids = JSONField(default=list, blank=True)
	mcq_list = models.TextField(blank=True, default="")

	class Meta:
		ordering = ("id",)

	def clean(self):
		from django.core.exceptions import ValidationError

		if not self.question_count and not self.percentage:
			raise ValidationError("Either question_count or percentage is required.")

	def __str__(self) -> str:  # pragma: no cover - trivial
		parts = [self.subject]
		if self.chapter:
			parts.append(self.chapter)
		if self.sub_chapter:
			parts.append(self.sub_chapter)
		if self.section:
			parts.append(self.section)
		return " > ".join(parts)


class MockTestQuestion(models.Model):
	mock_test = models.ForeignKey(MockTest, related_name="questions", on_delete=models.CASCADE)
	mock_test_tab = models.ForeignKey(MockTestTab, related_name="questions", on_delete=models.CASCADE)
	mcq_model = models.CharField(max_length=100, blank=True, null=True, db_index=True)
	mcq_id = models.IntegerField(db_index=True)
	order = models.PositiveIntegerField(default=0, db_index=True)
	marks = models.FloatField(default=1.0)
	negative_marks = models.FloatField(default=0.0)
	added_manually = models.BooleanField(default=False, db_index=True)

	class Meta:
		ordering = ("order", "id")
		unique_together = ("mock_test", "mcq_model", "mcq_id")

	def __str__(self) -> str:  # pragma: no cover - trivial
		return f"MCQ {self.mcq_id} ({self.marks}/{self.negative_marks})"
