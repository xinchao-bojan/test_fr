# Generated by Django 3.2 on 2021-06-10 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20210610_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='date_start',
            field=models.DateField(editable=False, verbose_name='Дата начала опроса'),
        ),
    ]
