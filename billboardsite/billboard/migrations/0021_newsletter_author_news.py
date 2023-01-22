# Generated by Django 4.1.5 on 2023-01-22 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billboard', '0020_userprofile_appr_replies_alerts'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='author_news',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='auth_newsletters', to=settings.AUTH_USER_MODEL, verbose_name='Автор новостей'),
        ),
    ]
