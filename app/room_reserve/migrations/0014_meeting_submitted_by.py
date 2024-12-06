# Generated by Django 4.2.7 on 2024-12-05 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0013_alter_meeting_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='submitted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Submitted By'),
        ),
    ]
