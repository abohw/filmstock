# Generated by Django 3.1.4 on 2021-02-21 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20210119_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='format',
            field=models.CharField(db_index=True, default='35mm', max_length=10),
            preserve_default=False,
        ),
    ]