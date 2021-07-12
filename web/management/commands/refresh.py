from django.core.management import BaseCommand
from django.conf import settings
from web.models import Camera, Film, followedFilm
from django.utils import timezone
from django.db.models import Min
import pytz

class Command(BaseCommand):
    help = 'what'

    def refreshFilm(self):

        for film in Film.objects.all():

            for stock in film.stock.filter(lastSeen__gt=(timezone.now() - timezone.timedelta(minutes=60))):

                if stock.price < film.lowLast30d or film.lowLast30d == 0.00:
                    film.lowLast30d = stock.price
                    film.lowUpdatedOn = timezone.now()
                    print('new low price for %s' % (film.name))

                if stock.price < film.lowAllTime or film.lowAllTime == 0.00:
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
            print('deleting %s from %s' % (camera.name, camera.source))
            camera.delete()
            x += 1

        print('%s records deleted' % (x))