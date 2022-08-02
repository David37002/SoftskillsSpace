from django.db import models

from softskillspace.utils.models import NamedTimeBasedModel


class Country(NamedTimeBasedModel):
    iso_code = models.CharField(
        max_length=3,
        help_text="2 digit iso code.",
    )

    dialling_code = models.CharField(
        default="",
        verbose_name="dialling code",
        max_length=10,
        help_text="This will be used for the mobile number prefix.",
    )

    cities = models.TextField(
        null=True,
        blank=True,
        help_text="One city per line",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "countries"

    @property
    def city_lists(self):
        """
        Return all the cities inputed in the database as a list
        """
        cities = self.cities.replace("\r", "").split("\n")
        cities = sorted(set(cities))
        return cities
