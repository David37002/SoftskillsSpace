from django.db.models.signals import post_save
from django.dispatch import receiver

from tutor.models import Tutor, TutorAvailability


@receiver(post_save, sender=Tutor)
def create_tutor_availablilty(sender, instance, created, **kwargs):
    """createsthe tutor availabliity model automatically when a new tutor is created"""
    if created:
        weekday = "09:00 - 17:00"

        TutorAvailability.objects.create(
            tutor=instance,
            monday=weekday,
            tuesday=weekday,
            wednesday=weekday,
            thursday=weekday,
            friday=weekday,
        )
