from rest_framework import viewsets, permissions
from django.utils import timezone

from .models import (Poll, Question, Choice, 
                     TextAnswer, ChoiceAnswer, MultiChoiceAnswer)
from .mixins import PermissionMixin
from .permissions import IsAdminUserOrReadOnly
from .serializers import (PollsSerializer, QuestionsSerializer, ChoicesSerializer, 
                          TextAnswerSerializer, ChoiceAnswerSerializer, MultiChoiceAnswerSerializer, ActiveSerializer)

from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
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
        # self.request.session["test"] = test
        key = self.request.session.session_key
        request = self.request.session.get("test")
        a = 2
        return request


class ChoiceAnswerViewSet(viewsets.ModelViewSet):

    permissions = [permissions.AllowAny]
    serializer_class = ChoiceAnswerSerializer


class MultiChoiceAnswer(viewsets.ModelViewSet):

    permissions = [permissions.AllowAny]
    serializer_class = MultiChoiceAnswerSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)


@api_view(["POST"])
def text_answer(request):
    user_id = request.session.get("user_id", None)
    if not user_id:
        request.session["user_id"] = 124124124124 # генерируемое число
    serializer = TextAnswerSerializer(data=request.data)
    if serializer.is_valid():
            serializer.validate_user_id(data=request.data, user_id=user_id)
            serializer.save(user_id=user_id)
            return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def choice_answer(request):
    user_id = request.session.get("user_id", None)
    if not user_id:
        request.session["user_id"] = 124124124124 # генерируемое число
    serializer = ChoiceAnswerSerializer(data=request.data)
    if serializer.is_valid():
            serializer.validate_user_id(data=request.data, user_id=user_id)
            serializer.save(user_id=user_id)
            return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def multi_choice_answer(request):
    user_id = request.session.get("user_id", None)
    if not user_id:
        request.session["user_id"] = 124124124124 # генерируемое число
    serializer = MultiChoiceAnswerSerializer(data=request.data)
    if serializer.is_valid():
            serializer.validate_user_id(data=request.data, user_id=user_id)
            serializer.save(user_id=user_id)
            return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
