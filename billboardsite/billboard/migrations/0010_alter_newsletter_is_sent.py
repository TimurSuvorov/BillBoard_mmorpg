# Generated by Django 4.1.5 on 2023-01-15 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0009_alter_userprofile_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='is_sent',
            field=models.BooleanField(default=False, verbose_name='Отправлено'),
        ),
    ]
