# Generated by Django 3.1.4 on 2021-07-08 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0027_auto_20210306_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='followedfilm',
            name='in_stock',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
