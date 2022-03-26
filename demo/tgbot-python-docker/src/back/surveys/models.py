from django.db import models

# Create your models here.


class Survey(models.Model):
    survey_name = models.CharField(max_length=45)
    from_user = models.CharField(max_length=45)  # Связь между таблицей юзеров
    to_user = models.CharField(max_length=45)  # Связь между таблицей юзеров
    questions = models.ForeignKey('SurveyGroup', on_delete=models.CASCADE)
    class Meta:
        db_table = "survey"
        verbose_name = "Опрос"
        verbose_name_plural = "Опрос"


class Answer(models.Model):
    questions = models.ManyToManyField('SurveyGroup')
    title = models.CharField(max_length=4096)
    created = models.DateTimeField(auto_now_add=True)


class SurveyGroup(models.Model):
    group_name = models.CharField(max_length=45)
    questions = models.ManyToManyField('SurveyQuestions', blank=True)

    def get_questions(self):
        return self.questions

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группа"

    def __str__(self):
        return self.group_name

class SurveyQuestions(models.Model):
    title = models.CharField(max_length=4096)
    survey_group = models.ManyToManyField('SurveyGroup', blank=True)
    class Meta:
        verbose_name = "Вопросы"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"{self.id}. {self.title}"