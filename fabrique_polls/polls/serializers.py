from rest_framework import serializers

from django.utils import timezone

from .models import (Poll, Question, Choice, TextAnswer,
                     ChoiceAnswer, MultiChoiceAnswer)


class ChoicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ("id", "text", )
        read_only_fields = ("id", )


class QuestionsSerializer(serializers.ModelSerializer):

    choices = ChoicesSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ("id", "text", "question_type", "choices", )
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


class TextAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextAnswer
        fields = ("user_id", "question", "text")

    def validate_question(self, value):
        if value.question_type != Question.TXT:
            raise serializers.ValidationError("Ответ должен быть на вопрос типа Text")
        return value

    def validate(self, data):
        user_id = data["user_id"]
        question = data["question"]
        if TextAnswer.objects.filter(user_id=user_id, question=question).exists():
            raise serializers.ValidationError("Вы уже отвечали на этот вопрос")
        return data


class ChoiceAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChoiceAnswer
        fields = ("user_id", "question", "choice")

    def validate_question(self, value):
        if value.question_type != Question.CHC:
            raise serializers.ValidationError("Ответ должен быть на вопрос типа Choice")
        return value

    def validate(self, data):
        user_id = data["user_id"]
        question = data["question"]
        if ChoiceAnswer.objects.filter(user_id=user_id, question=question).exists():
            raise serializers.ValidationError("Вы уже отвечали на этот вопрос")
        try:
            Choice.objects.get(pk=data["choice"].id, question=data["question"])
        except Choice.DoesNotExist:
            raise serializers.ValidationError("id choice должно должно принадлежать к конкретному вопросу")
        else:
            return data


class MultiChoiceAnswerSerializer(serializers.ModelSerializer):

    choices = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = MultiChoiceAnswer
        fields = ["question", "user_id", "choices"]

    def validate_question(self, value):
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
        question = data["question"]
        user_id = data["user_id"]
        if MultiChoiceAnswer.objects.filter(user_id=user_id, question=question).exists():
            raise serializers.ValidationError("Вы уже отвечали на этот вопрос")
        try:
            [Choice.objects.get(pk=value, question=question) for value in self.choices]
        except Choice.DoesNotExist:
            raise serializers.ValidationError("id одного из choices не принадлежить нужному вопросу")
        return data

    def create(self, validated_data):
        choices = self.choices
        question = validated_data["question"]
        user_id = validated_data["user_id"]
        objs = [MultiChoiceAnswer(choice_id=value, user_id=user_id, question_id=question.id)
                for value in choices]
        MultiChoiceAnswer.objects.bulk_create(objs)
        return {"user_id": user_id, "question": question, "choices": choices}


class FinishedQuestionsSerializer(serializers.ModelSerializer):

    choices = ChoicesSerializer(many=True, required=False)
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ("id", "text", "choices", "answers")

    def get_answers(self, obj):
        user_id = self.context["user_id"]
        if obj.question_type == Question.TXT:
            answer = TextAnswer.objects.get(question=obj, user_id=user_id)
            return answer.text
        elif obj.question_type == Question.CHC:
            answer = Choice.objects.get(question=obj, single_choice__user_id=user_id)
            return answer.text
        elif obj.question_type == Question.MCH:
            answers = Choice.objects.filter(question=obj, multi_choices__user_id=user_id).values("text")
            return answers


class FinishedPollSerializer(serializers.ModelSerializer):

    questions = FinishedQuestionsSerializer(many=True, required=False)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Poll
        fields = ("title", "description", "questions", "user_id")
