# Generated by Django 3.1.4 on 2021-01-20 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20210119_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmstock',
            name='quantity',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]