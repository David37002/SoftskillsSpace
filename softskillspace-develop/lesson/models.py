import uuid

import auto_prefetch
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.utils.dateformat import format as date_fmt

from softskillspace.utils.choices import LessonStatus
from softskillspace.utils.html import rating_to_html
from softskillspace.utils.models import TimeBasedModel


class Lesson(TimeBasedModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    tutor = auto_prefetch.ForeignKey(
        "tutor.Tutor",
        on_delete=models.CASCADE,
        null=True,
    )

    student = auto_prefetch.ForeignKey(
        "home.CustomUser", on_delete=models.CASCADE, null=True
    )

    subject = auto_prefetch.ForeignKey(
        "subject.Subject", on_delete=models.CASCADE, null=True
    )

    location = models.TextField(
        max_length=100,
        null=True,
        blank=True,
        default="Online",
    )

    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(default=timezone.now, editable=False)
    price_per_hour = models.PositiveSmallIntegerField(default=0)

    duration_minutes = models.PositiveSmallIntegerField(
        help_text="Duration in minutes", default=60
    )
    status = models.CharField(
        max_length=15,
        default=LessonStatus.Pending,
        choices=LessonStatus.choices,
    )
    created_by = auto_prefetch.ForeignKey(
        "home.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_by",
    )
    meeting_link = models.TextField(null=True, blank=True)

    def __str__(self):
        date_time = date_fmt(self.start_datetime, "j M Y, P")
        return f"{date_time} - {self.subject}"

    def save(self, *args, **kwargs):
        self.end_datetime = self.start_datetime + timezone.timedelta(
            minutes=self.duration_minutes
        )
        return super().save(*args, **kwargs)

    @property
    def total_cost(self):
        """
        Calculate the total cost for hours chosen
        """
        cost = (self.duration_minutes / 60) * self.price_per_hour
        return round(cost, 2)

    @property
    def duration(self):
        """
        Calculate the total cost for hours chosen
        """
        hr = self.duration_minutes // 60
        mins = self.duration_minutes % 60

        return f"{hr}h {mins}m"

    @property
    def start_date_format(self):
        """
        Start date formatted in a friendly way
        """
        date_time = date_fmt(self.start_datetime, "j M Y, P")
        return date_time


class Review(TimeBasedModel):
    lesson = auto_prefetch.OneToOneField(
        "lesson.Lesson",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"start_datetime__lte": timezone.now()},
    )
    rating = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(null=True, blank=True, max_length=150)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        date_time = date_fmt(self.created_at, "j M Y, P")
        word = truncatechars(self.comment, 50)

        return f"{date_time} - {word}"

    @property
    def star_rating(self):
        """Converts number rating to html font awesome icon"""
        return rating_to_html(self.rating, show_rating=False)
