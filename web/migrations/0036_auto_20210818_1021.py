# Generated by Django 3.1.4 on 2021-08-18 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0035_auto_20210807_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='type',
            field=models.CharField(choices=[('bw', 'Black & white'), ('cn', 'Color negative'), ('cp', 'Color positive'), ('ci', 'Color (instant)')], db_index=True, max_length=10),
        ),
    ]
