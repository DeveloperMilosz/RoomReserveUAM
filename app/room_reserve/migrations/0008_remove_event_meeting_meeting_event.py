# Generated by Django 4.2.7 on 2024-11-03 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0007_remove_event_meetings_event_meeting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='meeting',
        ),
        migrations.AddField(
            model_name='meeting',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='room_reserve.event', verbose_name='Event'),
        ),
    ]
