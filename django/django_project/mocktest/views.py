from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from mocktest.models import MockTest
from mocktest.services.mock_generator import MockTestGeneratorService


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
