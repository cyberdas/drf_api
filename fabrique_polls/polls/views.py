from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from django.utils import timezone

from .models import Poll, Question, Choice
from .permissions import IsAdminUserOrReadOnly
from .serializers import (PollsSerializer, QuestionsSerializer, ChoicesSerializer,
                          FinishedPollSerializer, TextAnswerSerializer, ChoiceAnswerSerializer,
                          MultiChoiceAnswerSerializer)
from .utils import get_answers, get_voted_polls


class ActiveViewSet(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = PollsSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        date = timezone.now()
        return Poll.objects.filter(end_date__gt=date)


class PollsViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAdminUser]
    serializer_class = PollsSerializer

    def get_queryset(self):
        return Poll.objects.all()


class QuestionsViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAdminUser]
    serializer_class = QuestionsSerializer

    def get_queryset(self):
        queryset = Question.objects.filter(poll_id=self.kwargs.get("poll_id"))
        return queryset

    def perform_create(self, serializer):
        poll = get_object_or_404(Poll, pk=self.kwargs.get("poll_id"))
        serializer.save(poll=poll)


class ChoicesViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAdminUser]
    serializer_class = ChoicesSerializer

    def get_queryset(self):
        queryset = Choice.objects.filter(question_id=self.kwargs.get("question_id"))
        return queryset

    def perform_create(self, seralizer):
        question = get_object_or_404(Question, pk=self.kwargs.get("question_id"))
        seralizer.save(question=question)


@api_view(["POST"])
def text_answer(request):
    serializer = TextAnswerSerializer
    return get_answers(request, serializer)


@api_view(["POST"])
def choice_answer(request):
    serializer = ChoiceAnswerSerializer
    return get_answers(request, serializer)


@api_view(["POST"])
def multi_choice_answer(request):
    serializer = MultiChoiceAnswerSerializer
    return get_answers(request, serializer)


@api_view(["POST"])
def get_finished_polls(request):
    user_id = request.POST.get("user_id", None)
    if not user_id:
        raise ValidationError({"Ошибка": "Передайте user_id"})
    voted_polls = get_voted_polls(request)
    if voted_polls.exists():
        serializer = FinishedPollSerializer(
            voted_polls, many=True, context={"user_id": user_id})
        return Response(serializer.data, status=HTTP_200_OK)
    raise ValidationError({"Ошибка": "Вы еще не прошли полностью ни один опрос"})
