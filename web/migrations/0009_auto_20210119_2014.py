# Generated by Django 3.1.4 on 2021-01-20 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20210119_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmstock',
            name='price',
            field=models.DecimalField(db_index=True, decimal_places=2, default=0, max_digits=7),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='filmPrice',
        ),
    ]
