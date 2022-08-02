from django.contrib import admin

from blog.models import Blog, BlogImage, Category


class BlogImageInline(admin.StackedInline):
    model = BlogImage


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["author", "name", "created_at"]
    ordering = ["created_at"]
    search_fields = ["name", "author"]
    inlines = [BlogImageInline]
    autocomplete_fields = ["author"]
    readonly_fields = ["slug"]
    list_filter = ["category"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    ordering = ["-created_at"]
    search_fields = ["name"]
    readonly_fields = ["bg_class"]
