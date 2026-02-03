import re

from django.core.exceptions import ValidationError
from django.db import models


class Property(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    currency = models.CharField(default="USD", max_length=200)
    price = models.IntegerField(null=True, blank=True)
    url = models.URLField(blank=False, null=False)
    object_id = models.IntegerField(unique=True, blank=False, null=False)
    address = models.CharField(max_length=500, blank=False, null=False)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)


    class Meta:
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["address"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["object_id"],
                name="unique_property_object_id"
            )
        ]


    def __str__(self):
        return self.title

    def extract_object_id(url: str) -> int:
        match = re.search(r'/(\d+)-', url)
        if not match:
            raise ValidationError("Cannot extract object_id from URL")
        return int(match.group(1))

    def clean(self):
        if not self.object_id:
            self.object_id = self.extract_object_id(self.url)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
