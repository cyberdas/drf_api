from rest_framework import viewsets, permissions

from .models import Poll, Question
from .permissions import IsAdminUserOrReadOnly
from .serializers import PollsSerializer, QuestionsSerializer


class PollsViewSet(viewsets.ModelViewSet):

    queryset = Poll.objects.all()
    serializer_class = PollsSerializer
    # permission_classes = [permissions.IsAdminUser]

# url = poll/id/questions/id
# все вопросы нужного опроса
# 
class QuestionsViewSet(viewsets.ModelViewSet):

    serializer_class = QuestionsSerializer

    def get_queryset(self):
        queryset = Question.objects.filter(poll_id=self.kwargs.get('poll_id'))
        return queryset


# class ChoicesViewSet(viewsets.ModelViewSet):

    # serializer_class = 