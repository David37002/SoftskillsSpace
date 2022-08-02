import auto_prefetch
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django_resized import ResizedImageField
from django.utils import timezone

from softskillspace.utils.choices import Gender, MailingListType
from softskillspace.utils.media import get_image_upload_path
from softskillspace.utils.models import NamedTimeBasedModel, TimeBasedModel



class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(TimeBasedModel, AbstractUser):
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    about = models.TextField(max_length=500, null=True, blank=True)
    email = models.EmailField(verbose_name="email address", unique=True)
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    country = auto_prefetch.ForeignKey(
        "location.Country", on_delete=models.SET_NULL, null=True, blank=True
    )
    gender = models.CharField(
        max_length=15, choices=Gender.choices, null=True, blank=True
    )
    profile_pic = ResizedImageField(
        upload_to=get_image_upload_path,
        blank=True,
        verbose_name="Profile Picture",
        null=True,
    )
    verified = models.BooleanField(default=False)

    objects = UserManager()

    class Meta(auto_prefetch.Model.Meta):
        ordering = ["first_name", "last_name"]
        verbose_name = "user"

    def __str__(self):
        return self.get_full_name() or self.email

    @property
    def image_url(self):
        """return image if it exists otherwise use a default"""
        if self.profile_pic:
            return self.profile_pic.url

        return f"{settings.STATIC_URL}images/avatar/default_avatar.png"

    @property
    def is_tutor(self):
        """Return true if user is a registered tutor"""
        return hasattr(self, "tutor")

    @property
    def is_instructor(self):
        """Return true if user is a registered instructor"""
        return hasattr(self, "instructor")


class MailingListCategory(NamedTimeBasedModel):
    name = models.CharField(
        max_length=20,
        unique=True,
        default=MailingListType.NewsLetter,
        choices=MailingListType.choices,
    )

    class Meta:
        verbose_name_plural = "mailing list categories"


class MailingList(TimeBasedModel):
    email = models.EmailField(max_length=30)
    categories = models.ManyToManyField("home.MailingListCategory")

    def __str__(self):
        return self.email


class UserStatistic(TimeBasedModel):
    user = auto_prefetch.OneToOneField(
        "home.CustomUser", on_delete=models.CASCADE)
    skill_point = models.PositiveBigIntegerField(default=0)
    wallet_amount = models.PositiveBigIntegerField(default=0)
    referral = models.PositiveSmallIntegerField(default=0)
    completed_lesson = models.PositiveSmallIntegerField(default=0)
    completed_course = models.PositiveSmallIntegerField(default=0)
    total_earning = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ["user__first_name", "user__last_name"]

    def __str__(self):
        return str(self.user)
