# Generated by Django 4.2.7 on 2024-12-05 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0014_meeting_submitted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='is_rejected',
            field=models.BooleanField(default=False, verbose_name='is rejected'),
        ),
    ]
