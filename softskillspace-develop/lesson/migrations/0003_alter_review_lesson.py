# Generated by Django 4.0 on 2022-05-02 20:06

import datetime

import auto_prefetch
import django.db.models.deletion
from django.db import migrations
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("lesson", "0002_alter_review_lesson"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="lesson",
            field=auto_prefetch.OneToOneField(
                blank=True,
                limit_choices_to={
                    "start_datetime__lte": datetime.datetime(
                        2022, 5, 2, 20, 6, 7, 201196, tzinfo=utc
                    )
                },
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="lesson.lesson",
            ),
        ),
    ]
