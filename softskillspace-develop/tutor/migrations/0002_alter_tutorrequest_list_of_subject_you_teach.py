# Generated by Django 4.0 on 2022-05-04 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tutor", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tutorrequest",
            name="list_of_subject_you_teach",
            field=models.TextField(),
        ),
    ]