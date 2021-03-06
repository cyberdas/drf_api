from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("polls", views.PollsViewSet, basename="polls")
router.register(r"polls/(?P<poll_id>\d+)/questions", views.QuestionsViewSet, basename="questions")  # все вопросы одного опроса
router.register(r"polls/(?P<poll_id>\d+)/questions/(?P<question_id>\d+)/choices", views.ChoicesViewSet, basename="choices")
router.register("text-answer", views.TextAnswerViewSet, basename="text_answer")
router.register("choice-answer", views.ChoiceAnswerViewSet, basename="choice_answer")
router.register("multi-choice-answer", views.MultiChoiceAnswer, basename="multi_choice_answer")

urlpatterns = [
    path("v1/", include(router.urls))  # добавить ответы пользователя
]
