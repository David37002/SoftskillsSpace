from django.contrib import admin

from lesson.models import Lesson, Review


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        "tutor",
        "student",
        "subject",
        "start_datetime",
        "status",
        "total_cost",
    ]
    list_filter = ["start_datetime", "status"]
    ordering = ["created_at"]
    search_fields = ["location"]
    readonly_fields = ["uuid"]
    autocomplete_fields = ["tutor", "student", "subject", "created_by"]
    list_select_related = ["tutor__user", "student", "subject"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["created_at", "comment", "rating"]
    list_filter = ["created_at", "rating"]
    ordering = ["created_at"]
    search_fields = ["comment"]
