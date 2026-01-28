from django.db import models


class Property(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    price = models.CharField(max_length=200, blank=False, null=False)
    url = models.URLField(unique=True, blank=False, null=False)
    address = models.CharField(max_length=500, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title