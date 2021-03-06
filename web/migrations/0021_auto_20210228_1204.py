# Generated by Django 3.1.4 on 2021-02-28 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0020_auto_20210227_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='lowAllTime',
            field=models.DecimalField(db_index=True, decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AddField(
            model_name='film',
            name='lowLast30d',
            field=models.DecimalField(db_index=True, decimal_places=2, default=0.0, max_digits=7),
        ),
    ]