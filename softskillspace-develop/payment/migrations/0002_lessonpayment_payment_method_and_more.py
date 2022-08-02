# Generated by Django 4.0 on 2022-05-03 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="lessonpayment",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("stripe", "Stripe"),
                    ("flutterwave", "Flutterwave"),
                    ("point", "Soft Point"),
                ],
                default="stripe",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="lessonpayment",
            name="payment_type",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="lessonpayment",
            name="receipt_url",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="lessonpayment",
            name="signature",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="lessonpayment",
            name="amount_paid",
            field=models.CharField(default="0", max_length=15),
        ),
    ]
