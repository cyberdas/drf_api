from django.contrib import admin

from .models import Poll, Question, Choice, TextAnswer, ChoiceAnswer, MultiChoiceAnswer


class ChoiceAnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "user_id", "choice")


class TextAnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "user_id", "text")


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class ChoiceAdmin(admin.ModelAdmin):
    model = Choice
    list_display = ("question", "text")


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


class PollAdmin(admin.ModelAdmin):
    inlines = (QuestionInline, )
    list_display = ("pk", "title", "description", "start_date")
    readonly_fields = ["start_date"]


class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoiceInline, )
    list_display = ("id", "text", "question_type")


admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TextAnswer, TextAnswerAdmin)
admin.site.register(ChoiceAnswer, ChoiceAnswerAdmin)
