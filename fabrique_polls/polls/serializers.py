from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import (Poll, Question, Choice, TextAnswer, 
                     ChoiceAnswer, MultiChoiceAnswer)


class ActiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ["id", "description", "start_date", "end_date"]


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
        validators = [
            UniqueTogetherValidator(
                queryset=TextAnswer.objects.all(),
                fields=["question", "user_id"],
                message="Вы уже отвечали на этот вопрос"
                )
        ]

    def validate_question(self, value):
        # username = str(self.request.session.session_key) + '@dummy.com'
        # request = self.context.get("request")
        # session = request.session.get("my_session")
        if value.question_type != Question.TXT:
            raise serializers.ValidationError("Ответ должен быть на вопрос типа Text")
        return value



class ChoiceAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChoiceAnswer
        fields = ("user_id", "question", "choice")
        validators = [
            UniqueTogetherValidator(
                queryset=ChoiceAnswer.objects.all(),
                fields=["question", "user_id"],
                message="Вы уже отвечали на этот вопрос"
                )
        ]

    def validate_question(self, value):
        if value.question_type != Question.CHC:
            raise serializers.ValidationError("Ответ должен быть на вопрос типа Choice")
        return value

    def validate(self, data):
        try:
            choice = Choice.objects.get(pk=data["choice"].id, question=data["question"])
        except Choice.DoesNotExist:
            raise serializers.ValidationError("id choice должно должно принадлежать к конкретному вопросу")
        else:
            return data


class MultiChoiceAnswerSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField()
    choices = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = MultiChoiceAnswer
        fields = ["question", "user_id", "choices"]
        validators = [
            UniqueTogetherValidator(
                queryset=MultiChoiceAnswer.objects.all(),
                fields=["question", "user_id"],
                message="Вы уже отвечали на этот вопрос"
                )
        ]
    # проблема в этом 
    # def to_internal_value(self, data):
        # choices = [int(i) for i in data["choices"].split(",")]
        # self.choices = choices
        # return data

    def validate_question(self, value): # questuion type потому что инт
        if value.question_type != Question.MCH:
            raise serializers.ValidationError("Ответ должен быть на вопрос типа MultiChoice")
        return value

    def validate_choices(self, value):
        try:
            choices = [int(i) for i in value[0].split(",")]
        except ValueError:
            raise serializers.ValidationError("Неверный формат ввода")
        else:
            if len(choices) < 2:
                raise serializers.ValidationError("Выберите несколько вариантов")
        self.choices = choices
        return value

    def validate(self, data):
        try:
           check = [Choice.objects.get(pk=value, question=data["question"]) for value in self.choices]
        except Choice.DoesNotExist:
            raise serializers.ValidationError("id одного из choices не принадлежить нужному вопросу")
        return data

    def create(self, validated_data):
        choices = self.choices
        question = validated_data["question"]
        user_id = int(validated_data["user_id"])
        objs = [MultiChoiceAnswer(choice_id=value, user_id=user_id, question_id=question.id)
            for value in choices]
        MultiChoiceAnswer.objects.bulk_create(objs)
        return {"user_id": user_id, "question": question, "choices": choices}


class VotedPollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ""