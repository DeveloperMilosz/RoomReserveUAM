# Generated by Django 4.2.7 on 2024-11-01 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0005_meeting_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='meetings',
            field=models.ManyToManyField(blank=True, related_name='events', to='room_reserve.meeting', verbose_name='Meetings'),
        ),
    ]