from django.contrib import admin

from chat.models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    ordering = ["-id"]
    list_filter = ["created_at", "visible"]
    filter_horizontal = ["participants"]
    readonly_fields = ["uuid"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["chat", "sender", "created_at", "preview"]
    ordering = ["-created_at"]
    list_filter = ["created_at", "visible"]
    search_fields = ["text"]
    readonly_fields = ["uuid"]
    list_select_related = ["chat", "sender"]
