# Generated by Django 5.1.1 on 2024-10-08 10:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share_food', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='available_until',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 11, 10, 53, 16, 612285, tzinfo=datetime.timezone.utc)),
        ),
    ]
