# Generated by Django 4.0 on 2022-05-04 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0007_category_bg_class_alter_blog_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="bg_class",
            field=models.CharField(
                blank=True,
                choices=[
                    ("bg-danger", "Danger"),
                    ("bg-dark", "Dark"),
                    ("bg-dribbble", "Dribbble"),
                    ("bg-facebook", "Facebook"),
                    ("bg-google", "Google"),
                    ("bg-info", "Info"),
                    ("bg-instagram", "Instagram"),
                    ("bg-light", "Light"),
                    ("bg-linkedin", "LinkedIn"),
                    ("bg-orange", "Orange"),
                    ("bg-pinterest", "Pinterest"),
                    ("bg-primary", "Primary"),
                    ("bg-purple", "Purple"),
                    ("bg-secondary", "Secondary"),
                    ("bg-skype", "Skype"),
                    ("bg-success", "Success"),
                    ("bg-transparent", "Transparent"),
                    ("bg-twitter", "Twitter"),
                    ("bg-warning", "Warning"),
                    ("bg-white", "White"),
                    ("bg-youtube", "YouTube"),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
