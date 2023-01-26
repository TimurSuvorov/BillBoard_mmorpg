# Generated by Django 4.1.5 on 2023-01-22 13:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0018_alter_userprofile_aboutme_alter_userprofile_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='title',
            field=models.CharField(db_index=True, error_messages={'unique': 'Такое объявление уже есть'}, max_length=254, unique=True, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='title',
            field=models.CharField(db_index=True, error_messages={'unique': 'Новость с таким заголовком уже есть'}, max_length=254, unique=True, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_news_subscribe',
            field=models.BooleanField(default=True, verbose_name='Подписка на новостную рассылку'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_replies_alerts',
            field=models.BooleanField(default=True, verbose_name='Оповещение о новых отликах'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='nickname',
            field=models.CharField(error_messages={'unique': 'Никнейм занят'}, help_text='Никнейм должен быть буквенно-цифровым и начинаться с букву', max_length=16, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z]+[0-9a-zA-Z]*$', 'Никнейм должен быть буквенно-цифровым и начинаться с букву')], verbose_name='Никнейм'),
        ),
    ]