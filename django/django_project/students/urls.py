from django.urls import path

from students import views

urlpatterns = [
    path("world-state/", views.world_state, name="world_state"),
    path("question-update/", views.question_update, name="question_update"),
]
