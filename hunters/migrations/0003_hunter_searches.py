# Generated by Django 3.1.4 on 2020-12-30 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_remove_savedsearch_hunter'),
        ('hunters', '0002_auto_20201229_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='hunter',
            name='searches',
            field=models.ManyToManyField(to='web.savedSearch'),
        ),
    ]
