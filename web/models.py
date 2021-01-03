from django.db import models
from hunters.models import Hunter

import django_filters

# Create your models here.

class Camera(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    source = models.CharField(max_length=255, db_index=True)
    store = models.CharField(max_length=255, blank=True, default=None, null=True)
    url = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(decimal_places=2, max_digits=7, db_index=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    lastSeen = models.DateTimeField(auto_now_add=True, db_index=True)
    new = models.BooleanField(default=True, db_index=True)

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
        ('brooklyn', 'Brooklyn Film Camera'),
        ('austin_camera', 'Austin Camera'),
        ('keh', 'KEH Camera'),
        ('etsy', 'Etsy'),
    ))

    sort = django_filters.OrderingFilter(
        label='Sort by:',
        empty_label='Recently added',
        choices=(
            ('-price', 'Price (High to Low)'),
            ('price', 'Price (Low to High)'),
            ('source', 'Source (A to Z)'),
            ('-source', 'Source (Z to A)'),
        ),
    )

    class Meta:
        model = Camera
        fields = ['name', 'price', 'source',]


class savedSearch(models.Model):
    hunter = models.ForeignKey(Hunter, blank=True, on_delete=models.CASCADE, related_name='searches')
    name = models.CharField(max_length=255, blank=True, default=None, null=True, db_index=True)
    terms = models.CharField(max_length=255, blank=True, default=None, null=True, db_index=True)
    source = models.CharField(max_length=255, blank=True, default=None, null=True, db_index=True)
    price_min = models.CharField(max_length=8, default=None, blank=True, null=True, db_index=True)
    price_max = models.CharField(max_length=8, default=None, blank=True, null=True, db_index=True)
    sort = models.CharField(max_length=255, blank=True, default=None, null=True, db_index=True)
    url = models.CharField(max_length=255, blank=True, default=None, null=True, db_index=True)

    is_subscribed = models.BooleanField(default=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return "%s" % (self.name)
