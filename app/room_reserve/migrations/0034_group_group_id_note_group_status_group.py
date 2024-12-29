# Generated by Django 4.2.7 on 2024-12-29 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0033_meeting_is_canceled'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_id',
            field=models.IntegerField(default=1, verbose_name='group_id'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='note',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='room_reserve.group', verbose_name='Group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status',
            name='group',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='room_reserve.group', verbose_name='Group'),
            preserve_default=False,
        ),
    ]