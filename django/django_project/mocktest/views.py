from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from mocktest.models import MockTest
from mocktest.services.mock_generator import MockTestGeneratorService, resolve_config_mcqs


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
