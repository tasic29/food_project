# Generated by Django 5.1.2 on 2024-10-10 07:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share_food', '0004_alter_userprofile_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='available_until',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 13, 7, 15, 29, 696815, tzinfo=datetime.timezone.utc)),
        ),
    ]
