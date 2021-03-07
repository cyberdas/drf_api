from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from django.db.models import Q, Exists

from . models import Poll


def get_answers(request, serializer):
    my_serializer = serializer(data=request.data)
    if my_serializer.is_valid():
            my_serializer.save()
            return Response(my_serializer.data, status=HTTP_201_CREATED)
    return Response(my_serializer.errors, status=HTTP_400_BAD_REQUEST)


def get_voted_polls(request):
	user_id = int(request.POST["user_id"])
	queryset = Poll.objects.filter(
		questions__answer__user_id=user_id).filter(
		questions__choice_answer__user_id=user_id).filter(
		questions__milti_choice_answer__user_id=user_id)
	return queryset
