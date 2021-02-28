from django.core.management import BaseCommand
from django.conf import settings
from web.models import Camera, Film
from django.utils import timezone
from django.db.models import Min
import pytz

class Command(BaseCommand):
    help = 'what'

    def refreshFilm(self):

        for film in Film.objects.annotate(lowest=Min('stock__price')):

            if film.lowest is not None and (film.lowest < film.lowLast30d or film.lowLast30d == 0.00 or film.lowUpdatedOn < (timezone.now() - timezone.timedelta(days=30))):
                film.lowLast30d = film.lowest
                film.lowUpdatedOn = timezone.now()
                print('new low price for %s' % (film.name))

                if film.lowest < film.lowAllTime or film.lowAllTime == 0.00:
                    film.lowAllTime = film.lowest
                    print('new all time low price for %s' % (film.name))

                film.save()

    def handle(self, *args, **options):

        x = 0

        self.refreshFilm()

        for camera in Camera.objects.filter(lastSeen__lt=(timezone.now() - timezone.timedelta(hours=1))):
            print('deleting %s from %s' % (camera.name, camera.source))
            camera.delete()
            x += 1

        print('%s records deleted' % (x))