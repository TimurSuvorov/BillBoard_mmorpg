# Generated by Django 4.1.5 on 2023-01-16 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0010_alter_newsletter_is_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='pageviews',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров'),
        ),
    ]