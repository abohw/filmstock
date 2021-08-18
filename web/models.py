from django.db import models
from hunters.models import Hunter

import django_filters


class Source(models.Model):

    name = models.CharField(default=None, blank=True, null=True, max_length=255, db_index=True)
    short_name = models.CharField(max_length=255, db_index=True)
    city = models.CharField(default=None, blank=True, null=True, max_length=255, db_index=True)
    state = models.CharField(default=None, blank=True, null=True, max_length=255, db_index=True)
    country = models.CharField(default=None, blank=True, null=True, max_length=255, db_index=True)
    shipping = models.DecimalField(default=0, decimal_places=2, max_digits=7, db_index=True)
    url = models.CharField(default=None, blank=True, null=True, max_length=255, db_index=True)
    lastScrapeTotal = models.IntegerField(default=0, blank=True, null=True, db_index=True)

    def __str__(self):
        return self.short_name


class Film(models.Model):

    brand = models.CharField(max_length=10, db_index=True)
    name = models.CharField(max_length=50, db_index=True)
    iso = models.IntegerField(db_index=True)
    experimental = models.BooleanField(db_index=True, default=False)
    format = models.CharField(max_length=10, choices=[('35mm', '35mm'), ('120', '120'), ('instant', 'Instant'), ('large', 'Large format'), ('110', '110')], db_index=True)
    type = models.CharField(max_length=10, choices=[('bw', 'Black & white'), ('cn', 'Color negative'), ('cp', 'Color positive'), ('ci', 'Color (instant)'),], db_index=True)
    exposures = models.IntegerField(db_index=True, choices=[(36, '36'), (24, '24')])
    lowLast30d = models.DecimalField(decimal_places=2, null=True, max_digits=7, default=0.00, db_index=True)
    lowUpdatedOn = models.DateTimeField(default=None, null=True, db_index=True)
    lowAllTime = models.DecimalField(decimal_places=2, null=True, max_digits=7, default=0.00, db_index=True)

    @property
    def url(self):

        if self.exposures:
            return '/film/%s/%s/%s/%s/' % (self.brand, self.name.replace(' ', '-'), self.format, self.exposures)
        else:
            return '/film/%s/%s/%s/' % (self.brand, self.name.replace(' ', '-'), self.format)

    def __str__(self):
        return '%s %s (%s exp., %s)' % (self.brand, self.name, self.exposures, self.format)


class filmStock(models.Model):

    film = models.ForeignKey(Film, default=None, null=True, blank=True, on_delete=models.CASCADE, related_name='stock')
    name = models.CharField(max_length=255, db_index=True)
    source = models.ForeignKey(Source, blank=True, on_delete=models.CASCADE, related_name='stock')
    url = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(decimal_places=2, max_digits=7, default=0.00, null=True, db_index=True)
    quantity = models.IntegerField(default=0, db_index=True)
    lastSeen = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-price"]

    def __str__(self):
        return '%s (%s)' % (self.name, self.source.short_name)


class FilmFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='Film name contains:', lookup_expr='icontains')

    format = django_filters.MultipleChoiceFilter(choices=(
        ('35mm', '35mm'),
        ('120', 'Medium'),
        ('instant', 'Instant'),
    ))

    brand = django_filters.MultipleChoiceFilter(choices=(
        ('Kodak', 'Kodak'),
        ('Fujifilm', 'Fujifilm'),
        ('Ilford', 'Ilford'),
        ('Cinestill', 'Cinestill'),
        ('Polaroid', 'Polaroid'),
        ('Lomography', 'Lomography'),
        ('Foma', 'Foma'),
        ('Kentmere', 'Kentmere'),
    ))

    type = django_filters.MultipleChoiceFilter(choices=(
        ('bw', 'Black and white'),
        ('cn', 'Color negative'),
        ('cp', 'Color positive'),
    ))

    sort = django_filters.OrderingFilter(
        label='Sort by:',
        empty_label='Price (Low to High)',
        choices=(
            ('type', 'Film type'),
            ('format', 'Film format'),
            ('iso', 'ISO (Low to High)'),
            ('-iso', 'ISO (High to Low)'),
        ),
    )

    class Meta:
        model = Film
        fields = ['name', 'brand', 'format', 'type', ]


class Camera(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    source = models.CharField(max_length=255, db_index=True)
    store = models.CharField(max_length=255, blank=True, default=None, null=True)
    url = models.URLField(db_index=True)
    price = models.DecimalField(decimal_places=2, max_digits=7, db_index=True)
    image = models.URLField(default=None, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    lastSeen = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-createdAt"]

    def __str__(self):
        return self.name


class CameraFilter(django_filters.FilterSet):

    price = django_filters.RangeFilter(label='Price is between:')
    name = django_filters.CharFilter(label='Camera name contains:', lookup_expr='icontains')

    source = django_filters.MultipleChoiceFilter(choices=(
        ('precision', 'Precision Camera'),
        ('brooklyn', 'Brooklyn Film Camera'),
        ('austin_camera', 'Austin Camera'),
        ('keh', 'KEH Camera'),
        ('roberts', 'Used Photo Pro'),
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


class followedFilm(models.Model):
    hunter = models.ForeignKey(Hunter, blank=True, on_delete=models.CASCADE, related_name='follows')
    film = models.OneToOneField(Film, on_delete=models.CASCADE, related_name='follows')
    in_stock = models.BooleanField(default=True, db_index=True)
    is_subscribed = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return "%s %s" % (self.hunter.email, self.film.name)


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
        return "%s %s" % (self.hunter.email, self.name)


class emailTask(models.Model):
    time = models.DateTimeField(auto_now_add=True, db_index=True)
    sent = models.IntegerField(default=0)
    skipped = models.IntegerField(default=0)
    success = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return "%s (%s)" % (self.time, self.success)
