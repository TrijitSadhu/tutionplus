from django.urls import path

from mocktest import views

urlpatterns = [
    path("api/mocktests/<int:mocktest_id>/config/", views.mocktest_config_cached, name="mocktest_config_cached"),
    path("api/mocktests/<int:mocktest_id>/config/live/", views.mocktest_config_live, name="mocktest_config_live"),
    path("api/mocktests/<int:mocktest_id>/config/resolved/", views.mocktest_config_resolved, name="mocktest_config_resolved"),
    path("mocktests/<int:mocktest_id>/exam/", views.mocktest_runner, name="mocktest_runner"),
]
