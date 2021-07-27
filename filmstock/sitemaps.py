from django.contrib import sitemaps
from django.urls import reverse
from web.models import Film


class FilmSitemap(sitemaps.Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Film.objects.all()

    def location(self, obj):

        return obj.url


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home','film','help','signup']

    def location(self, item):
        return reverse(item)