from django.urls import path

from mocktest import views

urlpatterns = [
    path("api/mocktests/<int:mocktest_id>/config/", views.mocktest_config_cached, name="mocktest_config_cached"),
    path("api/mocktests/<int:mocktest_id>/config/live/", views.mocktest_config_live, name="mocktest_config_live"),
]
