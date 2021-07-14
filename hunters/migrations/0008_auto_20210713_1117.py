# Generated by Django 3.1.4 on 2021-07-13 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hunters', '0007_auto_20210713_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='hunter',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='hunter',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]