# Generated by Django 4.2.7 on 2025-01-05 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0041_remove_roomplan_x_position_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomplan',
            old_name='svg_shapes',
            new_name='svg_points',
        ),
    ]