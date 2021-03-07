from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("polls", views.PollsViewSet, basename="polls")
router.register(r"polls/(?P<poll_id>\d+)/questions", views.QuestionsViewSet, basename="questions")
router.register(r"polls/(?P<poll_id>\d+)/questions/(?P<question_id>\d+)/choices", views.ChoicesViewSet, basename="choices")
router.register("polls-active", views.ActiveViewSet, basename="active_polls")
router.register("polls-finished", views.FinishedViewSet, basename="finished_polls")
# router.register("text-answer", views.text_answer, basename="text_answer")
router.register("choice-answer", views.ChoiceAnswerViewSet, basename="choice_answer")
router.register("multi-choice-answer", views.MultiChoiceAnswer, basename="multi_choice_answer")

urlpatterns = [
    path("", include(router.urls)),
    path("text-answer/", views.text_answer, name="text_answer"),
    path("choice-anwer/", views.choice_answer, name="choice_answer"),
    path("multi-choice-anwer/", views.multi_choice_answer, name="multi_choice_answer")
]
