from django.core.management import BaseCommand
from django.conf import settings
from web.models import Camera
from django.utils import timezone
import pytz

class Command(BaseCommand):
    help = 'what'

    def handle(self, *args, **options):

        x = 0

        for camera in Camera.objects.filter(lastSeen__lt=(timezone.now() - timezone.timedelta(hours=2))):
            print('deleting %s from %s' % (camera.name, camera.source))
            camera.delete()
            x += 1

        print('%s records deleted' % (x))
