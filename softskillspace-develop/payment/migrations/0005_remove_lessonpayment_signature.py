# Generated by Django 4.0 on 2022-05-03 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0004_lessonpayment_name_on_card"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lessonpayment",
            name="signature",
        ),
    ]
