from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail

from softskillspace.utils.urls import get_url
from tutor.models import (Tutor, TutorAvailability, TutorQualification,
                          TutorRequest, TutorSubject)


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ["user", "rate_per_hour", "verified_at"]
    ordering = ["user"]
    search_fields = ["bio"]
    autocomplete_fields = ["user"]

    def log_addition(self, request, object, message):
        user = object.user
        url = get_url(request, "tutor:edit-tutor")

        msg = (
            f"Hi {user}\n"
            + "Your tutor account has just been created.\n\n"
            + f"Please visit {url} to update your tutor profile "
            + "so you can start getting bookings from students.\n\n"
            + "Kind Regards\n"
            + "Soft Skill Space team"
        )

        send_mail(
            subject="Soft Skill Space - Tutor profile created",
            message=msg,
            fail_silently=True,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        log_entry = super().log_addition(request, object, message)
        return log_entry


@admin.register(TutorQualification)
class TutorQualificationAdmin(admin.ModelAdmin):
    list_display = ["tutor", "institution_name", "course_taken", "start_date"]
    ordering = ["created_at"]
    list_filter = ["institution_type", "level"]
    search_fields = ["institution_name"]
    autocomplete_fields = ["tutor"]


@admin.register(TutorSubject)
class TutorSubjectAdmin(admin.ModelAdmin):
    list_display = ["tutor", "subject"]
    ordering = ["-created_at"]
    filter_horizontal = ["levels"]
    autocomplete_fields = ["tutor", "subject"]


@admin.register(TutorAvailability)
class TutorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ["tutor"]
    ordering = ["tutor"]


@admin.register(TutorRequest)
class TutorRequestAdmin(admin.ModelAdmin):
    list_display = ["full_legal_name", "email_address", "whatsapp_number"]
    search_fields = ["full_legal_name", "email_address"]
