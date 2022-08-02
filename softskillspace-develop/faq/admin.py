from django.contrib import admin

from faq.models import FAQ, FaqCategory


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    ordering = ["name"]
    search_fields = ["name", "content"]
    filter_horizontal = ["categories"]
    list_filter = ["categories", "created_at"]


@admin.register(FaqCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    ordering = ["name"]
    search_fields = ["name"]
