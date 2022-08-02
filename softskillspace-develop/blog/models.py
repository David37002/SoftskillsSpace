import random
from time import time

import auto_prefetch
from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from softskillspace.utils.choices import BootstrapBackground
from softskillspace.utils.media import get_image_upload_path
from softskillspace.utils.models import NamedTimeBasedModel, TimeBasedModel

# Create your models here.


class Category(NamedTimeBasedModel):
    bg_class = models.CharField(
        verbose_name="background class",
        max_length=20,
        null=True,
        blank=True,
        choices=BootstrapBackground.choices,
    )

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.bg_class:
            random_class = random.choice(BootstrapBackground.values)
            self.bg_class = random_class
        return super().save(*args, **kwargs)


class Blog(NamedTimeBasedModel):
    author = auto_prefetch.ForeignKey(
        "home.CustomUser",
        on_delete=models.CASCADE,
        limit_choices_to={
            "is_staff": True})
    content = RichTextField()
    category = auto_prefetch.ForeignKey(
        "blog.Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.id} - {self.name}"

    def save(self, *args, **kwargs):
        """
        Override save method. Add Slug on Save
        """
        if not self.slug:
            self.slug = f"{slugify(self.name)}-{time()}"
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Url Path to Blog detail Page
        """
        return reverse("blog:detail", kwargs={"slug": self.slug})

    @property
    def image_url(self):
        """
        First Image from the List of Blog Images
        """
        return self.blogimage_set.first().image_url()


class BlogImage(TimeBasedModel):
    blog = auto_prefetch.ForeignKey("blog.Blog", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_upload_path)

    def __str__(self):
        return f"{self.blog.name} image"

    def image_url(self):
        """
        Return url of the Image
        """
        return getattr(self.image, "url", None)
