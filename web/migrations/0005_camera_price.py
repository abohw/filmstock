# Generated by Django 3.1.4 on 2020-12-29 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20201228_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
            preserve_default=False,
        ),
    ]
