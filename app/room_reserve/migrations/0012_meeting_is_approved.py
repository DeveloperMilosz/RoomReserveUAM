# Generated by Django 4.2.7 on 2024-12-04 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0011_alter_roomattribute_attribute_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='is approved'),
        ),
    ]
