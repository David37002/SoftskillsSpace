# Generated by Django 4.0 on 2022-05-02 23:54

import datetime

import auto_prefetch
import django.db.models.deletion
from django.db import migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("lesson", "0006_alter_lesson_booked_by_alter_review_lesson"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="lesson",
            field=auto_prefetch.OneToOneField(
                blank=True,
                limit_choices_to={
                    "start_datetime__lte": datetime.datetime(
                        2022, 5, 2, 23, 54, 55, 731064, tzinfo=utc
                    )
                },
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="lesson.lesson",
            ),
        ),
    ]
