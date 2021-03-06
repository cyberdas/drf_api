from rest_framework import viewsets, permissions

from .models import (Poll, Question, Choice, 
                     TextAnswer, ChoiceAnswer, MultiChoiceAnswer)
from .mixins import PermissionMixin
from .permissions import IsAdminUserOrReadOnly
from .serializers import (PollsSerializer, QuestionsSerializer, ChoicesSerializer, 
                          TextAnswerSerializer, ChoiceAnswerSerializer, MultiChoiceAnswerSerializer)


class PollsViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = PollsSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Poll.objects.all()
        return Poll.objects.filter(active=True)


class QuestionsViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = QuestionsSerializer
 
    def get_queryset(self):
        queryset = Question.objects.filter(poll_id=self.kwargs.get("poll_id"))
        return queryset


class ChoicesViewSet(viewsets.ModelViewSet):

    serializer_class = [IsAdminUserOrReadOnly] 
    serializer_class = ChoicesSerializer

    def get_queryset(self):
        queryset = Choice.objects.filter(question_id=self.kwargs.get("question_id"))
        return queryset


class TextAnswerViewSet(viewsets.ModelViewSet):

    permissions = [permissions.AllowAny]
    serializer_class = TextAnswerSerializer


class ChoiceAnswerViewSet(viewsets.ModelViewSet):

    permissions = [permissions.AllowAny]
    serializer_class = ChoiceAnswerSerializer


class MultiChoiceAnswer(viewsets.ModelViewSet):

    permissions = [permissions.AllowAny]
    serializer_class = MultiChoiceAnswerSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)
