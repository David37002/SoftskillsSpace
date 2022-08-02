import auto_prefetch
from django.db import models
from django.utils import timezone

from softskillspace.utils.models import TimeBasedModel


class TutorPromotion(TimeBasedModel):
    tutor = auto_prefetch.OneToOneField(
        "tutor.Tutor", on_delete=models.CASCADE)
    amount_paid = models.PositiveSmallIntegerField(default=0)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()

    class Meta:
        ordering = ["start_date"]

    @property
    def duration(self):
        """
        Calculate the duration using start and end date
        """
        return self.end_date - self.start_date

    def __str__(self):
        return str(self.tutor)
