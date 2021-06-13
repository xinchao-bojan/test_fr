# Generated by Django 3.2 on 2021-06-11 12:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0003_alter_interview_date_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='respondents',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('TYPING', 'текстовый ответ'), ('CHOICE', 'выбор варианта')], max_length=50, verbose_name='Тип'),
        ),
    ]