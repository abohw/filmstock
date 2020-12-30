# Generated by Django 3.1.4 on 2020-12-30 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0006_remove_savedsearch_hunter'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedsearch',
            name='hunter',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='searches', to='hunters.hunter'),
            preserve_default=False,
        ),
    ]
