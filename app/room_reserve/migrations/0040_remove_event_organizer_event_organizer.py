# Generated by Django 4.2.7 on 2025-01-04 15:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0039_alter_meeting_lecturers_alter_meeting_submitted_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='organizer',
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ManyToManyField(blank=True, limit_choices_to={'user_type__in': ['Lecturer', 'Organizer']}, related_name='lecturer_event', to=settings.AUTH_USER_MODEL, verbose_name='Organizers/Lecturers'),
        ),
    ]
