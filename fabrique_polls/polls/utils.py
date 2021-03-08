from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from django.db.models import Q, Exists, OuterRef

from . models import Poll, Question


def get_answers(request, serializer):
	my_serializer = serializer(data=request.data)
	if my_serializer.is_valid():
		my_serializer.save()
		return Response(my_serializer.data, status=HTTP_201_CREATED)
	return Response(my_serializer.errors, status=HTTP_400_BAD_REQUEST)


def get_voted_polls(request):
	user_id = request.POST.get("user_id", None)
	response_queryset = Poll.objects.filter(Q(questions__answer__user_id=user_id)
                                   | Q(questions__choices__single_choice__user_id=user_id)
                                   | Q(questions__choices__multi_choices__user_id=user_id))
	no_response_queryset = Question.objects.filter(poll=OuterRef('pk')).exclude(Q(choices__single_choice__user_id=user_id)
                                                                    | Q(answer__user_id=user_id)
                                                                    | Q(choices__multi_choices__user_id=user_id))
	queryset = response_queryset.exclude(Exists(no_response_queryset)).distinct()															
	return queryset
