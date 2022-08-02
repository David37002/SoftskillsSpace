from ckeditor.fields import RichTextField
from django.db import models

from softskillspace.utils.models import NamedTimeBasedModel


class FaqCategory(NamedTimeBasedModel):
    class Meta:
        verbose_name_plural = "faq categories"


class FAQ(NamedTimeBasedModel):
    content = RichTextField(null=True)
    categories = models.ManyToManyField("faq.FaqCategory", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
