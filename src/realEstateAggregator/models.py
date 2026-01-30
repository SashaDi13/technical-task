from django.db import models


class Property(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    currency = models.CharField(max_length=200)
    price = models.IntegerField(null=True, blank=True)
    url = models.URLField(unique=True, blank=False, null=False)
    address = models.CharField(max_length=500, blank=False, null=False)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["address"]),
        ]