from django.core.validators import MinValueValidator
from django.db import models


class Poll(models.Model):

    title = models.CharField(max_length=200, verbose_name="Название опроса")
    start_date = models.DateTimeField(verbose_name='Дата создания')
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return self.title


class Question(models.Model):

    TXT = "Text"
    CHC = "Choice"
    MCH = "Multichoice"
    choices = [
        (TXT, "Ответьте текстом"),
        (CHC, "Выберите один вариант"),
        (MCH, "Выберите несколько вариантов")
    ]
    text = models.TextField(verbose_name="Текст вопроса")
    poll = models.ForeignKey(
        Poll, related_name="questions",
        on_delete=models.CASCADE, verbose_name="Опрос")
    question_type = models.CharField(
        max_length=11, choices=choices,
        verbose_name="Тип вопроса")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"{self.poll.id} - {self.question_type}"


class Choice(models.Model):

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE,
        related_name="choices", verbose_name="Вопрос")
    text = models.CharField(max_length=64, verbose_name="Текст")

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return f"{self.text}"


class TextAnswer(models.Model):

    user_id = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name="id пользователя")
    question = models.ForeignKey(
        Question, related_name="answer",
        on_delete=models.CASCADE, verbose_name="Вопрос")
    text = models.TextField(verbose_name="Текст ответа")

    class Meta:
        verbose_name = "Текстовый ответ пользователя"
        verbose_name_plural = "Текстовые ответы пользователя"
        constraints = [models.UniqueConstraint(
            fields=["user_id", "question"], name="unique_text_answer")]


class ChoiceAnswer(models.Model):

    user_id = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name="id пользователя")
    question = models.ForeignKey(
        Question, related_name="choice_answer", on_delete=models.CASCADE,
        verbose_name="Вопрос")
    choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE,
        verbose_name="Выбор пользователя", related_name="single_choice")

    class Meta:
        verbose_name = "Выбор пользователя"
        verbose_name_plural = "Выбор одного варианта"
        constraints = [models.UniqueConstraint(
            fields=["user_id", "question"], name="unique_choice_answer")]


class MultiChoiceAnswer(models.Model):

    user_id = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name="id пользователя")
    choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, related_name="multi_choices")
    question = models.ForeignKey(
        Question, related_name="multi_choice_answer", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Выбор нескольких вариантов"
        verbose_name_plural = "Выбор нескольких вариантов"
        constraints = [models.UniqueConstraint(
            fields=["user_id", "choice"], name="unique_multi_choice_answer")]
