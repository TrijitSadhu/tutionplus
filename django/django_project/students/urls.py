from django.urls import path

from students import views

urlpatterns = [
    path("world/", views.world_home, name="world_home"),
    path("world-state/", views.world_state, name="world_state"),
    path("question-update/", views.question_update, name="question_update"),
    path("leaderboard/<int:mock_test_id>/", views.leaderboard, name="leaderboard"),
    path(
        "cinematic-race/<int:mock_test_id>/",
        views.cinematic_race,
        name="cinematic_race",
    ),
]
