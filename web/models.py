from django.db import models

import django_filters

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

class CameraFilter(django_filters.FilterSet):

#    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
#    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    price = django_filters.RangeFilter(label='Price is between:')

    name = django_filters.CharFilter(label='Camera name contains:', lookup_expr='icontains')

    source = django_filters.MultipleChoiceFilter(choices=(
        ('bh', 'B&H'),
        ('precision', 'Precision Camera'),
        ('austin_camera', 'Austin Camera'),
        ('keh', 'KEH Camera'),
    ))

    class Meta:
        model = Camera
        fields = ['name', 'price', 'source',]
