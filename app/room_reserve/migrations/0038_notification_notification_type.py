# Generated by Django 4.2.7 on 2024-12-29 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0037_alter_notification_user_type_alter_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(blank=True, choices=[('message', 'message'), ('notification', 'notification')], max_length=50, null=True, verbose_name='Typ powiadomienia'),
        ),
    ]