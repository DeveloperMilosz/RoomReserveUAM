# Generated by Django 4.2.7 on 2024-12-29 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0035_remove_group_group_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Department'),
        ),
    ]
