# Generated by Django 3.1.4 on 2021-02-27 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0015_auto_20210227_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='format',
            field=models.CharField(choices=[('35mm', '35mm'), ('120', '120'), ('instant', 'Instant'), ('large', 'Large format'), ('110', '110')], db_index=True, max_length=10),
        ),
    ]
