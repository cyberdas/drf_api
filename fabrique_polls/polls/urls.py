from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("polls", views.PollsViewSet, basename="polls")
router.register(r"polls/(?P<poll_id>\d+)/questions", views.QuestionsViewSet, basename="questions")  # все вопросы одного опроса
# router.register(r"poll/(?P<poll_id>\d+)/questions/?P<question_id>/choices", views.ChoicesViewSet)

urlpatterns = [
    path("v1/", include(router.urls))  # добавить ответы пользователя
]
