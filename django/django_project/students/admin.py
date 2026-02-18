from django.contrib import admin

from bank.admin import admin_site
from students.models import (
    MockTestAttempt,
    Payment,
    QuestionAttempt,
    SectionAttempt,
    StudentProfile,
    SubjectPerformance,
)


@admin.register(StudentProfile, site=admin_site)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "active_exam", "is_paid", "created_at")
    list_filter = ("is_paid",)
    search_fields = ("user__username", "user__email")


@admin.register(Payment, site=admin_site)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "amount", "currency", "status", "transaction_id", "created_at")
    list_filter = ("status", "currency")
    search_fields = ("transaction_id", "provider_reference", "student__user__username", "student__user__email")
    raw_id_fields = ("student",)


@admin.register(SectionAttempt, site=admin_site)
class SectionAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "mock_test_attempt",
        "mock_test_tab",
        "started_at",
        "completed_at",
        "total_confused_questions",
        "average_confusion_score",
    )
    list_filter = ("mock_test_tab",)
    raw_id_fields = ("mock_test_attempt", "mock_test_tab")


@admin.register(QuestionAttempt, site=admin_site)
class QuestionAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "section_attempt",
        "mock_test_question",
        "selected_option",
        "option_change_count",
        "mark_for_review_count",
        "time_spent_seconds",
        "confusion_flag",
        "confusion_score",
    )
    list_filter = ("confusion_flag", "is_marked_for_review")
    raw_id_fields = ("section_attempt", "mock_test_question")


@admin.register(MockTestAttempt, site=admin_site)
class MockTestAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "exam",
        "mock_test",
        "total_confused_questions",
        "confusion_index",
        "created_at",
    )
    raw_id_fields = ("student", "exam", "mock_test")


@admin.register(SubjectPerformance, site=admin_site)
class SubjectPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "exam",
        "subject",
        "strength_score",
        "previous_strength_score",
        "mastery_streak",
        "average_confusion_index",
        "total_confused_questions",
        "updated_at",
    )
    list_filter = ("exam", "subject")
    raw_id_fields = ("student", "exam")
