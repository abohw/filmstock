# Generated by Django 3.1.4 on 2020-12-31 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hunters', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hunter',
            name='referral_code',
        ),
    ]