from django.contrib import admin
from .models import Survey, SurveyGroup, SurveyQuestions, Answer
# Register your models here.


class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        'survey_name',
        'from_user',
        'to_user',
        'questions'
    )


class SurveyGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name',)


class SurveyQuestionsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )
    filter_horizontal = ('survey_group',)


# class AnswerAdmin(admin.ModelAdmin):
#     question_list = SurveyGroup.get_questions()
#     list_display = ('title',)
#     filter_horizontal = ('question_list',)


admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyGroup, SurveyGroupAdmin)
admin.site.register(SurveyQuestions, SurveyQuestionsAdmin)
# admin.site.register(Answer, AnswerAdmin)