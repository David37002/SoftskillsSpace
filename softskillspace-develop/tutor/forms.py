from django import forms
from django.utils import timezone

from home.models import CustomUser
from lesson.models import Lesson
from softskillspace.utils.choices import LessonDuration
from softskillspace.utils.forms import CssForm
from subject.models import Subject
from tutor.models import Tutor, TutorQualification, TutorRequest

MINIMUM_BOOKING_DATETIME = timezone.now() + timezone.timedelta(hours=3)
MINIMUM_BOOKING_DATETIME = timezone.datetime.strftime(
    MINIMUM_BOOKING_DATETIME, "%Y-%m-%dT%H:%m"
)


class TutorBookALessonForm(CssForm, forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            "student",
            "subject",
            "location",
            "start_datetime",
            "duration_minutes",
            "price_per_hour",
        ]

    student = forms.ModelChoiceField(
        required=True,
        queryset=CustomUser.items.none(),
        empty_label=None,
        label="Student name",
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


class TutorForm(CssForm, forms.ModelForm):
    class Meta:
        model = Tutor
        exclude = ["verified_at", "user", "id_documents_provided", "visible"]

    bio = forms.CharField(max_length=60, widget=forms.TextInput())
    profile_pic = forms.ImageField(required=False)


class TutorRequestForm(CssForm, forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "max": "2014-01-01"})
    )

    name_of_subject_you_teach = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "4"})
    )

    whatsapp_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "minlength": "10"}))

    class Meta:
        model = TutorRequest
        exclude = ["visible"]


class TutorAvailabilityForm(CssForm, forms.Form):
    monday_from = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )
    monday_to = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )

    tuesday_from = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )
    tuesday_to = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )

    wednesday_from = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )
    wednesday_to = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )

    thursday_from = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )
    thursday_to = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )

    friday_from = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )
    friday_to = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )

    saturday_from = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )
    saturday_to = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )

    sunday_from = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )
    sunday_to = forms.TimeField(
        required=False, widget=forms.TimeInput(attrs={"type": "time"})
    )


class TutorQualificationForm(CssForm, forms.ModelForm):
    class Meta:
        model = TutorQualification
        fields = [
            "institution_name", "institution_type", "course_taken",
            "level", "start_date", "end_date"
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
