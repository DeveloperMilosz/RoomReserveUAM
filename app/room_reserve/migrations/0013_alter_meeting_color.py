# Generated by Django 4.2.7 on 2024-12-05 00:00

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0012_meeting_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='color',
            field=colorfield.fields.ColorField(default='#2873FF', image_field=None, max_length=25, samples=None),
        ),
    ]
