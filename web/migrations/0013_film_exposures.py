# Generated by Django 3.1.4 on 2021-02-21 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20210221_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='exposures',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=False,
        ),
    ]
