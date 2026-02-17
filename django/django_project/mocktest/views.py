from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from mocktest.models import MockTest
from mocktest.services.mock_generator import MockTestGeneratorService, resolve_config_mcqs
from django.shortcuts import redirect
from mocktest.forms import ExamForm
from mocktest.models import Exam


def mocktest_config_cached(request, mocktest_id: int):
	mock = get_object_or_404(MockTest, id=mocktest_id)
	payload = mock.config_json or {}
	if not payload:
		# Fallback to live snapshot if cache empty
		service = MockTestGeneratorService()
		payload = service._snapshot_config(mock)
	return JsonResponse(payload, safe=False)


def mocktest_config_live(request, mocktest_id: int):
	mock = get_object_or_404(MockTest, id=mocktest_id)
	service = MockTestGeneratorService()
	payload = service._snapshot_config(mock)
	return JsonResponse(payload, safe=False)


def mocktest_config_resolved(request, mocktest_id: int):
	"""Return config plus resolved MCQ records (bulk fetched by new_id/id)."""
	mock = get_object_or_404(MockTest, id=mocktest_id)
	service = MockTestGeneratorService()
	config = mock.config_json or {}
	if not config:
		config = service._snapshot_config(mock)
	payload = resolve_config_mcqs(config)
	return JsonResponse(payload, safe=False)


def mocktest_runner(request, mocktest_id: int):
	"""Serve the exam UI shell; data is fetched client-side from resolved API."""
	return render(request, "mocktest/mocktest_exam.html", {"mocktest_id": mocktest_id})


# ===============================
# EXAM MANAGEMENT SYSTEM START
# ===============================


def exam_update_view(request, exam_id: int):
	exam = get_object_or_404(
		Exam.objects.select_related("segment").prefetch_related("mock_tests"), id=exam_id
	)

	if request.method == "POST":
		form = ExamForm(request.POST, instance=exam, request=request)
		if form.is_valid():
			form.save()
			return redirect(request.path)
	else:
		form = ExamForm(instance=exam, request=request)

	return render(request, "mocktest/exam_update.html", {"form": form, "exam": exam})
