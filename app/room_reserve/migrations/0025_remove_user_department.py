# Generated by Django 4.2.7 on 2024-12-16 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0024_merge_0020_status_note_0023_alter_notification_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='department',
        ),
    ]