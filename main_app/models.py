from django.db import models
from custom_user.models import CustomUser


class Interview(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название опроса')
    date_start = models.DateField(verbose_name='Дата начала опроса', editable=False)
    date_finish = models.DateField(verbose_name='Дата конца опроса')
    description = models.TextField(verbose_name='Описание')
    respondents = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    class Types(models.TextChoices):
        TYPING = ('TYPING', 'текстовый ответ')
        CHOICE = ('CHOICE', 'выбор варианта')

    type = models.CharField(max_length=50, choices=Types.choices, verbose_name='Тип')
    text = models.TextField(verbose_name='Текст вопроса')
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class TypingManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Question.Types.TYPING)


class Typing(Question):
    objects = TypingManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Question.Types.TYPING
        return super().save(*args, **kwargs)


class ChoiceManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Question.Types.CHOICE)


class ChoiceMore(models.Model):
    choice = models.OneToOneField('Choice', on_delete=models.CASCADE)
    multiple_answer = models.BooleanField(default=False)


class Choice(Question):
    objects = ChoiceManager()

    class Meta:
        proxy = True

    @property
    def more(self):
        return self.choicemore

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Question.Types.CHOICE
        return super().save(*args, **kwargs)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, verbose_name='Текст ответа')
    user_set = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.text
