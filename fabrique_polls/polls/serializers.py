from rest_framework import serializers
from django.utils import timezone
from datetime import datetime

from .models import (Poll, Question, Choice, TextAnswer, 
                     ChoiceAnswer, MultiChoiceAnswer)


class ChoicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ("id", "text", "question")
        read_only_fields = ("id", )

    def validate(self, data):
        question_id = data["question"].id
        if str(question_id) != self.context['request'].parser_context['kwargs']['question_id']:
            raise serializers.ValidationError("Поле question должно соответсововать id вопроса")
        return data


class QuestionsSerializer(serializers.ModelSerializer):
    
    choices = ChoicesSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ("id", "text", "question_type", "choices", "poll")
        read_only_fields = ("id", )

    def validate(self, data):
        poll_id = data["poll"].id
        if str(poll_id) != self.context['request'].parser_context['kwargs']['poll_id']:
            raise serializers.ValidationError("Поле poll должно соответсововать id опроса")
        return data


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

class TextAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextAnswer
        fields = ("user_id", "question", "text")

    # def validate_question(self, value):
        # if question.type != Question.TXT

class ChoiceAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChoiceAnswer
        fields = ("user_id", "question", "choice")

class MultiChoiceAnswerSerializer(serializers.ModelSerializer):

    choices = ChoicesSerializer(many=True)

    class Meta:
        model = MultiChoiceAnswer
        fields = ("user_id", "question", "choices")
