from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("polls", views.PollsViewSet, basename="polls")
router.register(r"polls/(?P<poll_id>\d+)/questions", views.QuestionsViewSet, basename="questions")
router.register(r"polls/(?P<poll_id>\d+)/questions/(?P<question_id>\d+)/choices", views.ChoicesViewSet, basename="choices")
router.register("polls-active", views.ActiveViewSet, basename="active_polls")

urlpatterns = [
    path("", include(router.urls)),
    path("text-answer/", views.text_answer, name="text_answer"),
    path("choice-answer/", views.choice_answer, name="choice_answer"),
    path("multi-choice-answer/", views.multi_choice_answer, name="multi_choice_answer"),
    path("polls-finished/", views.get_finished_polls, name="finished_polls")
]
