# Generated by Django 4.1.5 on 2023-01-25 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0022_userprofile_photoprofile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photoprofile',
            field=models.ImageField(default='', height_field='150', null=True, upload_to='photoprofile/', width_field='150'),
        ),
    ]
