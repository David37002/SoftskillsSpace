from django import forms
from django.utils import timezone

from lesson.models import Lesson
from softskillspace.utils.choices import LessonDuration
from softskillspace.utils.forms import CssForm
from subject.models import Subject
from tutor.models import Tutor

MINIMUM_BOOKING_DATETIME = timezone.now() + timezone.timedelta(hours=3)
MINIMUM_BOOKING_DATETIME = timezone.datetime.strftime(
    MINIMUM_BOOKING_DATETIME, "%Y-%m-%dT%H:%m"
)


class StudentBookALessonForm(CssForm, forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            "tutor",
            "subject",
            "location",
            "start_datetime",
            "duration_minutes",
            "price_per_hour",
        ]

    tutor = forms.ModelChoiceField(
        required=True,
        queryset=Tutor.items.all(),
        empty_label=None,
        label="Tutor name",
    )

    subject = forms.ModelChoiceField(
        required=True,
        queryset=Subject.items.all(),
        empty_label=None,
    )

    location = forms.CharField(
        max_length=200,
        min_length=6,
        help_text=(
            "Choose online if having the lesson online "
            + "or enter full address location if meeting physically"
        ),
        initial="Online",
        widget=forms.Textarea(
            attrs={
                "rows": 3,
            }
        ),
    )

    start_datetime = forms.DateTimeField(
        label="Start date and time",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "min": MINIMUM_BOOKING_DATETIME}
        ),
    )

    duration_minutes = forms.ChoiceField(
        label="Duration",
        choices=LessonDuration.choices,
        initial=LessonDuration.MIN_60)

    price_per_hour = forms.IntegerField(min_value=0)
