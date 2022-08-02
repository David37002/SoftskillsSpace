# Generated by Django 4.0 on 2022-05-03 16:08

from django.db import migrations, models

import softskillspace.utils.strings


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0006_lessonpayment_paid_tutor"),
    ]

    operations = [
        migrations.AddField(
            model_name="lessonpayment",
            name="reference_no",
            field=models.CharField(
                default=softskillspace.utils.strings.generate_ref_no,
                max_length=8),
        ),
        migrations.AlterField(
            model_name="lessonpayment",
            name="transaction_id",
            field=models.CharField(
                max_length=30),
        ),
    ]
