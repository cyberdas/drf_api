from rest_framework import viewsets, permissions
from django.utils import timezone

from .models import (Poll, Question, Choice, 
                     TextAnswer, ChoiceAnswer, MultiChoiceAnswer)
from .mixins import PermissionMixin
from .permissions import IsAdminUserOrReadOnly
from .serializers import (PollsSerializer, QuestionsSerializer, ChoicesSerializer, 
                          TextAnswerSerializer, ChoiceAnswerSerializer, MultiChoiceAnswerSerializer, ActiveSerializer)

from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.response import Response

class FinishedViewSet(viewsets.ModelViewSet):
    pass


class ActiveViewSet(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    
    serializer_class = PollsSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    
    def get_queryset(self):
        date = timezone.now()
        return Poll.objects.filter(end_date__gt=date)


class PollsViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.AllowAny]
    serializer_class = PollsSerializer

    def get_queryset(self):
        return Poll.objects.all()


class QuestionsViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.AllowAny]
    serializer_class = QuestionsSerializer
 
    def get_queryset(self):
        queryset = Question.objects.filter(poll_id=self.kwargs.get("poll_id"))
        return queryset


class ChoicesViewSet(viewsets.ModelViewSet):

    serializer_class = [permissions.AllowAny] 
    serializer_class = ChoicesSerializer

    def get_queryset(self):
        queryset = Choice.objects.filter(question_id=self.kwargs.get("question_id"))
        return queryset


class TextAnswerViewSet(viewsets.ModelViewSet):

    permissions = [permissions.AllowAny]
    serializer_class = TextAnswerSerializer

    def perform_create(self, serializer_class):
        pass

    
class ChoiceAnswerViewSet(viewsets.ModelViewSet):

    permissions = [permissions.AllowAny]
    serializer_class = ChoiceAnswerSerializer


class MultiChoiceAnswer(viewsets.ModelViewSet):

    permissions = [permissions.AllowAny]
    serializer_class = MultiChoiceAnswerSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)

# функция по ответу
@api_view(["GET", "POST"])
def test_func(request):
    a = 123
    if not request.session.exists(request.session.session_key):
        request.session.create() 
    request.session.save()
    username = str(request.session.session_key) + '@dummy.com'
    return Response(status=HTTP_200_OK)
