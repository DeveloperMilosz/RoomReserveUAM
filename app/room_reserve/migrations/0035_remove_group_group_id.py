# Generated by Django 4.2.7 on 2024-12-29 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0034_group_group_id_note_group_status_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='group_id',
        ),
    ]
