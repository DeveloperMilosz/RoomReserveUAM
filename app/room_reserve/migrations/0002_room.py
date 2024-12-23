# Generated by Django 4.2.7 on 2024-10-18 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=30, verbose_name='room number')),
                ('building_id', models.IntegerField(verbose_name='building id')),
                ('building_name', models.CharField(max_length=50, verbose_name='building name')),
                ('capacity', models.IntegerField(blank=True, null=True, verbose_name='capacity')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('is_updated', models.BooleanField(default=True, verbose_name='is updated')),
                ('room_supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='room supervisor')),
            ],
        ),
    ]
