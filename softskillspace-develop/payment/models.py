import auto_prefetch
from django.db import models

from softskillspace.utils.choices import (LessonPaymentStatus,
                                          PaymentMethodChoice)
from softskillspace.utils.models import TimeBasedModel
from softskillspace.utils.strings import generate_ref_no


class LessonPayment(TimeBasedModel):
    name_on_card = models.CharField(max_length=50, null=True)
    lesson = auto_prefetch.OneToOneField(
        "lesson.Lesson", on_delete=models.CASCADE, null=True, blank=True
    )
    reference_no = models.CharField(max_length=8, default=generate_ref_no)
    transaction_id = models.CharField(max_length=30)
    amount_paid = models.CharField(max_length=15, default="0")
    amount_gross = models.CharField(max_length=15, default="0")
    amount_fee = models.CharField(max_length=15, default="0")
    amount_net = models.CharField(max_length=15, default="0")
    status = models.CharField(
        max_length=15,
        choices=LessonPaymentStatus.choices,
        default=LessonPaymentStatus.Pending,
    )
    payment_type = models.CharField(max_length=15, null=True, blank=True)
    receipt_url = models.TextField(null=True, blank=True)
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethodChoice.choices,
        default=PaymentMethodChoice.Stripe,
    )
    paid_tutor = models.BooleanField(default=False)

    def __str__(self):
        return self.transaction_id
