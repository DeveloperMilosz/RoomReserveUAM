# Generated by Django 4.2.7 on 2024-12-26 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0032_group_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='is_canceled',
            field=models.BooleanField(default=False, verbose_name='Is Canceled'),
        ),
    ]