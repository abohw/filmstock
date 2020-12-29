from django.core.management import BaseCommand
from django.conf import settings
from web.models import Camera

from datetime import datetime

class Command(BaseCommand):
    help = 'what'

    def handle(self, *args, **options):

        x = 0

        for camera in Camera.objects.filter(lastSeen__lt=datetime.now()):
            camera.delete()
            x += 1

        print('%s records deleted' % (x))
