# Generated by Django 3.1.4 on 2021-02-28 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0021_auto_20210228_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='lowUpdatedOn',
            field=models.DateTimeField(db_index=True, null=True, default=None),
        ),
    ]
