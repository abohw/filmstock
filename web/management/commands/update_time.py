from django.core.management import BaseCommand
from django.conf import settings
from web.models import Camera
from django.utils import timezone
import pytz

from datetime import date
from datetime import datetime

class Command(BaseCommand):
    help = 'what'

    def handle(self, *args, **options):

        x = 0

        for camera in Camera.objects.all():
            camera.createdAt = datetime.combine(camera.createdAt, datetime.min.time())
            camera.save()
            x += 1

        print('%s records updated' % (x))
