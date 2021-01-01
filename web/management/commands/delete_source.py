from django.core.management import BaseCommand
from django.conf import settings
from web.models import Camera

class Command(BaseCommand):
    help = 'what'

    def add_arguments(self, parser):
        parser.add_argument('source', type=str)

    def handle(self, *args, **options):

        x = 0

        source = options['source']

        if Camera.objects.filter(source__exact=source):

            for camera in Camera.objects.filter(source__exact=source):
                print('deleting %s from %s' % (camera.name, camera.source))
                camera.delete()
                x += 1

        print('%s records deleted' % (x))
