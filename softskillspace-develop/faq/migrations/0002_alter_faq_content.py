# Generated by Django 3.2.13 on 2022-05-06 13:07

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("faq", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="faq",
            name="content",
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
