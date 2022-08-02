import auto_prefetch
from django.db import models
from django.utils.dateformat import format as date_fmt

from softskillspace.utils.choices import AcademicLevel, InstitutionType
from softskillspace.utils.models import TimeBasedModel


class Tutor(TimeBasedModel):
    user = auto_prefetch.OneToOneField(
        "home.CustomUser", on_delete=models.CASCADE)
    bio = models.TextField(max_length=60, null=True, blank=True)
    rate_per_hour = models.PositiveSmallIntegerField(default=0)

    # Verification info
    verified_at = models.DateTimeField(null=True, blank=True)
    id_documents_provided = models.TextField(null=True, blank=True)

    # Account details
    account_no = models.CharField(
        max_length=50, verbose_name="Account number", null=True, blank=True
    )
    sort_code = models.CharField(
        max_length=70,
        verbose_name="Bank name / Sort code",
        null=True,
        blank=True)

    street = models.CharField(max_length=100, null=True, blank=True)
    town = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    post_code = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return str(self.user)


class TutorQualification(TimeBasedModel):
    tutor = auto_prefetch.ForeignKey(
        "tutor.Tutor", on_delete=models.CASCADE, null=True)
    institution_name = models.CharField(max_length=100)
    institution_type = models.CharField(
        max_length=50, choices=InstitutionType.choices)
    course_taken = models.CharField(max_length=100)
    level = models.CharField(max_length=50, choices=AcademicLevel.choices)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return str(self.tutor)

    @property
    def date_range(self):
        """
        Properly formatted date range for rendering education section
        """
        start_date = date_fmt(self.start_date, "M Y")

        if self.end_date:
            end_date = date_fmt(self.end_date, "M Y")
        else:
            end_date = "present"

        return f"{start_date} - {end_date}"


class TutorSubject(TimeBasedModel):
    tutor = auto_prefetch.ForeignKey(
        "tutor.Tutor", on_delete=models.CASCADE, null=True)
    subject = auto_prefetch.ForeignKey(
        "subject.Subject", blank=True, on_delete=models.CASCADE, null=True
    )
    levels = models.ManyToManyField("subject.InstitutionClassification")

    class Meta:
        unique_together = ["tutor", "subject"]

    def __str__(self):
        subject = getattr(self.subject, "name", "")
        return f"{self.tutor} - {subject}"


class TutorAvailability(TimeBasedModel):
    tutor = auto_prefetch.OneToOneField(
        "tutor.Tutor", on_delete=models.CASCADE)
    monday = models.CharField(max_length=20, null=True, blank=True)
    tuesday = models.CharField(max_length=20, null=True, blank=True)
    wednesday = models.CharField(max_length=20, null=True, blank=True)
    thursday = models.CharField(max_length=20, null=True, blank=True)
    friday = models.CharField(max_length=20, null=True, blank=True)
    saturday = models.CharField(max_length=20, null=True, blank=True)
    sunday = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name_plural = "tutor availability"
        ordering = ["tutor"]

    def __str__(self):
        return str(self.tutor)


class TutorRequest(TimeBasedModel):
    full_legal_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email_address = models.EmailField()
    whatsapp_number = models.CharField(max_length=30)
    name_of_subject_you_teach = models.TextField()
    highest_academic_qualification = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Tutors Request"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_legal_name} is requesting to be a Tutor"
