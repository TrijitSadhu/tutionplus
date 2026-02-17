from django import forms
from django.utils.dateparse import parse_date

from mocktest.models import Exam, MockTest


# ===============================
# EXAM MANAGEMENT SYSTEM START
# ===============================


class ExamForm(forms.ModelForm):
    title = forms.CharField(required=False)
    exam = forms.CharField(required=False)
    mock_type = forms.ChoiceField(required=False)
    is_active = forms.ChoiceField(required=False)
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    min_questions = forms.IntegerField(required=False)
    max_questions = forms.IntegerField(required=False)
    min_marks = forms.FloatField(required=False)
    max_marks = forms.FloatField(required=False)

    class Meta:
        model = Exam
        fields = ["segment", "name", "year", "exam_date", "state", "mock_tests"]
        widgets = {
            "exam_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields["mock_type"].choices = [("", "All Types")] + list(MockTest.MOCK_TYPE_CHOICES)
        self.fields["is_active"].choices = [("", "Any Status"), ("true", "Active"), ("false", "Inactive")]

        base_qs = MockTest.objects.all().order_by("-created_at")
        filtered_qs = base_qs
        params = request.GET if request else {}

        title = params.get("title") if params else None
        if title:
            filtered_qs = filtered_qs.filter(title__icontains=title)

        exam = params.get("exam") if params else None
        if exam:
            filtered_qs = filtered_qs.filter(exam__icontains=exam)

        mock_type = params.get("mock_type") if params else None
        if mock_type:
            filtered_qs = filtered_qs.filter(mock_type=mock_type)

        is_active = params.get("is_active") if params else None
        if is_active in ("true", "false"):
            filtered_qs = filtered_qs.filter(is_active=is_active == "true")

        date_from_raw = params.get("date_from") if params else None
        date_to_raw = params.get("date_to") if params else None
        date_from = parse_date(date_from_raw) if date_from_raw else None
        date_to = parse_date(date_to_raw) if date_to_raw else None
        if date_from:
            filtered_qs = filtered_qs.filter(created_at__gte=date_from)
        if date_to:
            filtered_qs = filtered_qs.filter(created_at__lte=date_to)

        min_q = params.get("min_questions") if params else None
        max_q = params.get("max_questions") if params else None
        if min_q:
            try:
                filtered_qs = filtered_qs.filter(total_questions__gte=int(min_q))
            except (TypeError, ValueError):
                pass
        if max_q:
            try:
                filtered_qs = filtered_qs.filter(total_questions__lte=int(max_q))
            except (TypeError, ValueError):
                pass

        min_marks = params.get("min_marks") if params else None
        max_marks = params.get("max_marks") if params else None
        if min_marks:
            try:
                filtered_qs = filtered_qs.filter(total_marks__gte=float(min_marks))
            except (TypeError, ValueError):
                pass
        if max_marks:
            try:
                filtered_qs = filtered_qs.filter(total_marks__lte=float(max_marks))
            except (TypeError, ValueError):
                pass

        selected_ids = []
        if self.instance and self.instance.pk:
            selected_ids = list(self.instance.mock_tests.values_list("id", flat=True))

        if selected_ids:
            filtered_qs = filtered_qs | base_qs.filter(id__in=selected_ids)

        self.fields["mock_tests"].queryset = filtered_qs.distinct().order_by("title")
        if selected_ids:
            self.initial.setdefault("mock_tests", selected_ids)
        self.fields["mock_tests"].help_text = ""
