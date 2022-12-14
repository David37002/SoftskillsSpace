# Generated by Django 4.0 on 2022-05-02 23:48

import datetime

import auto_prefetch
import django.db.models.deletion
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("lesson", "0004_alter_review_lesson"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="booked_by",
            field=models.CharField(null=True, blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name="review",
            name="lesson",
            field=auto_prefetch.OneToOneField(
                blank=True,
                limit_choices_to={
                    "start_datetime__lte": datetime.datetime(
                        2022, 5, 2, 23, 48, 31, 986568, tzinfo=utc
                    )
                },
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="lesson.lesson",
            ),
        ),
    ]
