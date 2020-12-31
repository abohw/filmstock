from django.core.management import BaseCommand
from django.conf import settings
from django.utils import timezone
import pytz
from django.core import mail
from hunters.models import Hunter
from web.models import Camera
from django.template import loader


class Command(BaseCommand):
    help = 'what'

    def sourceCameras(self, search):

        cameras = Camera.objects.filter(createdAt__range=[timezone.now() - timezone.timedelta(hours=1), timezone.now()])

        if search.terms:
            cameras = cameras.filter(name__icontains=search.terms)

        if search.new:
            cameras = cameras.filter(new=search.new)

        if search.source:
            source = search.source
            source = source.replace('\'','').replace('[','').replace(']','').replace(',','')
            source = source.split(' ')
            cameras = cameras.filter(source__in=source)

        if search.price_min and search.price_max:
            cameras = cameras.filter(price__range=[float(search.price_min), float(search.price_max)])
        elif search.price_min:
            cameras = cameras.filter(price__gt=float(search.price_min))
        elif search.price_max:
            cameras = cameras.filter(price__lt=float(search.price_min))

        if search.sort:
            cameras = cameras.order_by(search.sort)
        else:
            cameras = cameras.order_by('-price')

        return cameras


    def handle(self, *args, **options):

        connection = mail.get_connection()

        connection.open()

        for hunter in Hunter.objects.filter(is_approved=True):

            searches = Hunter.searches.filter(is_subscribed=True)
            
            if searches:

                for search in searches:

                    cameras = self.sourceCameras(search)

                    if cameras:

                        html_message = loader.render_to_string(
                            'emails/new-camera.html',
                            {
                                'name': search.name,
                                'cameras': cameras,
                            }
                        )

                        message = ''
                        for camera in cameras:
                            message += '%s (%s)\n%s\n\n' % (camera.name, camera.price, camera.url)

                        mail.send_mail(
                            '%s: %s new camera(s)' % (search.name, cameras.count()),
                            'Filmstock\n\n%s' % (message),
                            'Filmstock <alerts@filmstock.app>',
                            [hunter.email],
                            fail_silently=True,
                            connection=connection,
                            html_message=html_message,
                        )

                        print('%s new cameras for %s, email sent to %s' % (cameras.count(), search.name, hunter.email))

                    else: print('no new cameras for %s, no email sent to %s' % (search.name, hunter.email))

        connection.close()
