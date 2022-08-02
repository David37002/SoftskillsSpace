from django.contrib import admin

from subject.models import InstitutionClassification, Subject, SubjectCategory


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name", "rank"]
    list_filter = ["categories", "classification"]
    ordering = ["name"]
    filter_horizontal = ["categories", "classification"]
    search_fields = ["name"]


@admin.register(InstitutionClassification, SubjectCategory)
class SubjectHelperAdmin(admin.ModelAdmin):
    list_display = ["name"]
    ordering = ["name"]
    search_fields = ["name"]
