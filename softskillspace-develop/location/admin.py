from django.contrib import admin

from location.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "iso_code", "dialling_code"]
    search_fields = ["name"]
    ordering = ["name"]
