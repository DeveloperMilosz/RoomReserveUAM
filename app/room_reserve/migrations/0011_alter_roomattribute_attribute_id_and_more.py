# Generated by Django 4.2.7 on 2024-11-24 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_reserve', '0010_roomattribute_remove_room_room_equipment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomattribute',
            name='attribute_id',
            field=models.CharField(max_length=100, verbose_name='attribute id'),
        ),
        migrations.AlterField(
            model_name='roomattribute',
            name='count',
            field=models.IntegerField(verbose_name='count'),
        ),
        migrations.AlterField(
            model_name='roomattribute',
            name='description_en',
            field=models.TextField(verbose_name='description (EN)'),
        ),
        migrations.AlterField(
            model_name='roomattribute',
            name='description_pl',
            field=models.TextField(verbose_name='description (PL)'),
        ),
    ]
