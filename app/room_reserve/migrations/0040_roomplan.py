# Generated by Django 4.2.7 on 2025-01-04 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0039_meeting_is_api_meeting_is_excel'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building_name', models.CharField(max_length=100)),
                ('floor', models.IntegerField()),
                ('x_position', models.IntegerField()),
                ('y_position', models.IntegerField()),
                ('plan_image', models.ImageField(upload_to='building_plans/')),
                ('room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='plan', to='room_reserve.room')),
            ],
        ),
    ]