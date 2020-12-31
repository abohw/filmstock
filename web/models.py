from django.db import models
from hunters.models import Hunter

import django_filters

# Create your models here.

class Camera(models.Model):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    store = models.CharField(max_length=255, blank=True, default=None, null=True)
    url = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    createdAt = models.DateTimeField(default=None, blank=True, null=True)
    lastSeen = models.DateTimeField(default=None, blank=True, null=True)
    new = models.BooleanField(default=True)

    class Meta:
        ordering = ["-createdAt"]

    def __str__(self):
        return self.name

class CameraFilter(django_filters.FilterSet):

    price = django_filters.RangeFilter(label='Price is between:')
    name = django_filters.CharFilter(label='Camera name contains:', lookup_expr='icontains')

    source = django_filters.MultipleChoiceFilter(choices=(
        ('bh', 'B&H'),
        ('precision', 'Precision Camera'),
        ('austin_camera', 'Austin Camera'),
        ('keh', 'KEH Camera'),
        ('etsy', 'Etsy'),
    ))

    new = django_filters.ChoiceFilter(label='Date added:', choices=(
        (True, 'Last 3 days'),
    ))

    sort = django_filters.OrderingFilter(
        label='Sort by:',
        choices=(
            ('-price', 'Price (High to Low)'),
            ('price', 'Price (Low to High)'),
            ('source', 'Source (A to Z)'),
            ('-source', 'Source (Z to A)'),
            ('-createdAt', 'Recently added'),
        ),
    )

    class Meta:
        model = Camera
        fields = ['name', 'price', 'source', 'new',]

class savedSearch(models.Model):
    hunter = models.ForeignKey(Hunter, blank=True, on_delete=models.CASCADE, related_name='searches')
    name = models.CharField(max_length=255, blank=True, default=None, null=True)
    terms = models.CharField(max_length=255, blank=True, default=None, null=True)
    source = models.CharField(max_length=255, blank=True, default=None, null=True)
    price_min = models.CharField(max_length=8, default=None, blank=True, null=True)
    price_max = models.CharField(max_length=8, default=None, blank=True, null=True)
    new = models.BooleanField(blank=True, default=False, null=True)
    sort = models.CharField(max_length=255, blank=True, default=None, null=True)
    url = models.CharField(max_length=255, blank=True, default=None, null=True)

    is_subscribed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % (self.name)
