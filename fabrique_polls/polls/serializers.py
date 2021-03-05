from rest_framework import serializers
from django.utils import timezone
from datetime import datetime

from .models import Poll, Question, Choice


class ChoicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ("id", "text", "question")
        read_only_fields = ("id", )


class QuestionsSerializer(serializers.ModelSerializer):
    
    choices = ChoicesSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ("id", "text", "question_type", "choices", "poll")
        read_only_fields = ("id", )


class PollsSerializer(serializers.ModelSerializer):

    questions = QuestionsSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ("id", "title", "start_date", "end_date", "description", "questions", )
        read_only_fields = ("id", )

    def validate_start_date(self, value):
        if self.instance and self.instance.start_date:
            raise serializers.ValidationError("Поле start_date изменить нельзя")
        if value <= timezone.now():
            raise serializers.ValidationError("Изменить дату старту опроса, она должна быть в будущем")
        return value

    def validate(self, data):
        start = data["start_date"] if "start_date" in data else self.instance.start_date
        end = data["end_date"] if "end_date" in data else self.instance.end_date
        if end <= start:
            raise serializers.ValidationError("Дата окончания должна быть после даты старта опроса")
        return data