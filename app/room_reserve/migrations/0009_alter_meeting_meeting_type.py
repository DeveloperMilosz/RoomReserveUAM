# Generated by Django 4.2.7 on 2024-11-03 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0008_remove_event_meeting_meeting_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='meeting_type',
            field=models.CharField(blank=True, choices=[('meeting', 'Spotkanie'), ('classgroup', 'Grupa zajęciowa')], max_length=50, null=True, verbose_name='Typ spotkania'),
        ),
    ]
