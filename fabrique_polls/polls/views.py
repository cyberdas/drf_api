from rest_framework import viewsets, permissions

from .models import (Poll, Question, Choice, 
                     TextAnswer, ChoiceAnswer, MultiChoiceAnswer)
from .mixins import PermissionMixin
from .permissions import IsAdminUserOrReadOnly
from .serializers import (PollsSerializer, QuestionsSerializer, ChoicesSerializer, 
                          TextAnswerSerializer, ChoiceAnswerSerializer, MultiChoiceAnswerSerializer)


class PollsViewSet(PermissionMixin):

    serializer_class = PollsSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Poll.objects.all()
        return Poll.objects.filter(active=True)


class QuestionsViewSet(PermissionMixin):

    serializer_class = QuestionsSerializer
 
    def get_queryset(self):
        queryset = Question.objects.filter(poll_id=self.kwargs.get("poll_id"))
        return queryset


class ChoicesViewSet(PermissionMixin):

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