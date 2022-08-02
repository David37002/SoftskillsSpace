from django.contrib import admin

from promotion.models import TutorPromotion


@admin.register(TutorPromotion)
class TutorPromotionAdmin(admin.ModelAdmin):
    list_display = ["tutor", "start_date", "duration"]
    ordering = ["-start_date"]
    list_filter = ["start_date"]
    autocomplete_fields = ["tutor"]
