# Generated by Django 4.2.7 on 2024-11-01 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0006_alter_event_meetings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='meetings',
        ),
        migrations.AddField(
            model_name='event',
            name='meeting',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event', to='room_reserve.meeting', verbose_name='Meeting'),
        ),
    ]