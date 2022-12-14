# Generated by Django 4.0.6 on 2022-08-01 04:23

import auto_prefetch
import datetime
from django.db import migrations
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0021_alter_review_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='lesson',
            field=auto_prefetch.OneToOneField(blank=True, limit_choices_to={'start_datetime__lte': datetime.datetime(2022, 8, 1, 4, 23, 51, 744977, tzinfo=utc)}, null=True, on_delete=django.db.models.deletion.CASCADE, to='lesson.lesson'),
        ),
    ]
