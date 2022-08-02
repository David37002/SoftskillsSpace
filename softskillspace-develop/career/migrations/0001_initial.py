# Generated by Django 4.0.6 on 2022-07-30 19:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=150)),
                ('type', models.CharField(choices=[('1', 'Full time'), ('2', 'Part time'), ('3', 'Internship')], max_length=10)),
                ('category', models.CharField(max_length=100)),
                ('last_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('filled', models.BooleanField(default=False)),
                ('salary', models.PositiveBigIntegerField(default=0)),
            ],
        ),
    ]
