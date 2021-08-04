from django.core.management import BaseCommand
from django.conf import settings
from web.models import Camera, Film, followedFilm, Source
from django.utils import timezone
from django.db.models import Min
import pytz

class Command(BaseCommand):
    help = 'what'

    def refreshFilm(self):

        for film in Film.objects.all():

            for stock in film.stock.filter(lastSeen__gt=(timezone.now() - timezone.timedelta(minutes=60))):

                if stock.price < film.lowLast30d or not film.lowLast30d:
                    film.lowLast30d = stock.price
                    film.lowUpdatedOn = timezone.now()
                    print('new low price for %s' % (film.name))

                if stock.price < film.lowAllTime or not film.lowAllTime:
                    film.lowAllTime = stock.price
                    print('new all time low price for %s' % (film.name))

            film.save()

    def handle(self, *args, **options):

        x = 0

        self.refreshFilm()

        for follow in followedFilm.objects.all():

            if follow.film.stock.filter(lastSeen__gt=(timezone.now() - timezone.timedelta(days=5))) is None:

                follow.in_stock = False
                follow.save()
                print('updated %s, not in stock' % (follow.film.name))

        for camera in Camera.objects.filter(lastSeen__lt=(timezone.now() - timezone.timedelta(hours=1))):

            source = Source.objects.get(short_name__exact=camera.source)

            if source.lastScrapeTotal > 0:
                print('deleting %s from %s' % (camera.name, camera.source))
                camera.delete()
                x += 1

            else:
                print('wanted to delete %s (%s), but might be broken' % (camera.name, camera.source))

        print('%s records deleted' % (x))