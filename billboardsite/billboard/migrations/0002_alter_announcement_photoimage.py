# Generated by Django 4.1.5 on 2023-02-03 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='photoimage',
            field=models.ImageField(blank=True, default='photoannouncement/photoannouncement_default.jpg', upload_to='photoannouncement/', verbose_name='Миниатюра объявления'),
        ),
    ]
