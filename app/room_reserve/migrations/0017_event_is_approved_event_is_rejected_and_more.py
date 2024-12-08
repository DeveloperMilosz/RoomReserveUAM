# Generated by Django 4.2.7 on 2024-12-08 18:01

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0016_event_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='is approved'),
        ),
        migrations.AddField(
            model_name='event',
            name='is_rejected',
            field=models.BooleanField(default=False, verbose_name='is rejected'),
        ),
        migrations.AlterField(
            model_name='event',
            name='color',
            field=colorfield.fields.ColorField(default='#0f2d66', image_field=None, max_length=25, samples=None),
        ),
    ]