from django.db import models

# Create your models here.

class Camera(models.Model):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    createdAt = models.DateField(default=None, blank=True, null=True)
    lastSeen = models.DateField(default=None, blank=True, null=True)
    new = models.BooleanField(default=True)

    class Meta:
        ordering = ["-createdAt"]

    def __str__(self):
        return self.name
