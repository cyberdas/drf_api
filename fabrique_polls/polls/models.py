from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Poll(models.Model):
    
    title = models.CharField(max_length=200, verbose_name="Название опроса")
    start_date = models.DateTimeField(verbose_name='Дата создания')
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    description = models.TextField(verbose_name="Описание")
    active = models.BooleanField(default=True, verbose_name="активный")

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


 # class Answer(models.Model):
    
    # poll
    # question
    # answer
    # id

# class Vote