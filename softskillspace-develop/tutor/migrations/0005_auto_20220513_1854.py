# Generated by Django 3.2.13 on 2022-05-13 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tutor", "0004_auto_20220506_1456"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tutor",
            name="account_no",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="Account number"),
        ),
        migrations.AlterField(
            model_name="tutor",
            name="city",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True),
        ),
        migrations.AlterField(
            model_name="tutor",
            name="sort_code",
            field=models.CharField(
                blank=True,
                max_length=70,
                null=True,
                verbose_name="Bank name / Sort code",
            ),
        ),
        migrations.AlterField(
            model_name="tutor",
            name="street",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True),
        ),
        migrations.AlterField(
            model_name="tutor",
            name="town",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True),
        ),
    ]
