from django.db.models.signals import post_save
from django.dispatch import receiver

from home.models import CustomUser, UserStatistic


@receiver(post_save, sender=CustomUser)
def create_user_statistic(sender, instance, created, **kwargs):
    """creates the user stats model automatically when a new user is created"""
    if created:
        UserStatistic.objects.create(
            user=instance,
            skill_point=0,
            referral=0,
            wallet_amount=0,
            total_earning=0,
            completed_lesson=0,
            completed_course=0,
        )
