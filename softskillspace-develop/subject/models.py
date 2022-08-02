from django.db import models

from softskillspace.utils.choices import InstitutionType
from softskillspace.utils.models import NamedTimeBasedModel


class Subject(NamedTimeBasedModel):
    categories = models.ManyToManyField("subject.SubjectCategory", blank=True)
    rank = models.FloatField(default=0)
    classification = models.ManyToManyField(
        "subject.InstitutionClassification", blank=True
    )
    subcategories = models.TextField(null=True, blank=True)

    @property
    def subcategory_lists(self):
        """
        Return all the subcategories inputed in the database as a list
        """
        subcategories = self.subcategories.replace("\r", "").split("\n")
        subcategories = sorted(set(subcategories))
        return subcategories


class SubjectCategory(NamedTimeBasedModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "categories"


class InstitutionClassification(NamedTimeBasedModel):
    name = models.CharField(
        max_length=50,
        choices=InstitutionType.choices,
        unique=True)
