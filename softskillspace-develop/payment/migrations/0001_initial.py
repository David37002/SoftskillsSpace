# Generated by Django 4.0 on 2022-05-02 12:49

import auto_prefetch
import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models

import softskillspace.utils.strings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("lesson", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LessonPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("visible", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "transaction_id",
                    models.CharField(
                        default=softskillspace.utils.strings.generate_ref_no,
                        max_length=8,
                    ),
                ),
                ("amount_paid", models.FloatField()),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("paid", "Paid")],
                        default="pending",
                        max_length=15,
                    ),
                ),
                (
                    "lesson",
                    auto_prefetch.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lesson.lesson",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
    ]
