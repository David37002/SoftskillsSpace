from django.contrib import admin

from payment.models import LessonPayment


@admin.register(LessonPayment)
class LessonPaymentAdmin(admin.ModelAdmin):
    list_display = ["transaction_id", "amount_paid", "status"]
    ordering = ["-created_at"]
    list_filter = ["created_at", "status"]
    readonly_fields = ["transaction_id", "receipt_url", "lesson"]
    search_fields = ["transaction_id"]
