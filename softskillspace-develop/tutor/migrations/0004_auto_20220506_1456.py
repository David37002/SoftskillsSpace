# Generated by Django 3.2.13 on 2022-05-06 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("subject",
         "0001_initial"),
        ("tutor",
            "0003_rename_list_of_subject_you_teach_tutorrequest_name_of_subject_you_teach",
         ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tutorsubject",
            options={},
        ),
        migrations.AlterUniqueTogether(
            name="tutorsubject",
            unique_together={("tutor", "subject")},
        ),
    ]
