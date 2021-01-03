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

        # yes i know the source search code is janky. i'll fix it later.
        if search.source and search.source != '[]':
            source = search.source
            source = source.replace('\'','').replace('[','').replace(']','').replace(',','')
            source = source.split(' ')
            cameras = cameras.filter(source__in=source)

        if search.price_min and search.price_max:
            cameras = cameras.filter(price__range=[float(search.price_min), float(search.price_max)])
        elif search.price_min:
            cameras = cameras.filter(price__gt=float(search.price_min))
        elif search.price_max:
            cameras = cameras.filter(price__lt=float(search.price_max))

        if search.sort:
            cameras = cameras.order_by(search.sort)
        else:
            cameras = cameras.order_by('-price')

        return cameras


    def handle(self, *args, **options):

        connection = mail.get_connection()

        connection.open()

        for hunter in Hunter.objects.filter(is_approved=True):

            searches = hunter.searches.filter(is_subscribed=True)

            if searches:

                for search in searches:

                    cameras = self.sourceCameras(search)
                    name = search.name

                    if cameras:

                        if len(name) > 24:
                            name = name[0:25] + '...'

                        html_message = loader.render_to_string(
                            'emails/new-camera.html',
                            {
                                'name': search.name,
                                'url': search.url,
                                'cameras': cameras,
                            }
                        )

                        message = ''
                        for camera in cameras:
                            message += '%s (%s)\n%s\n\n' % (camera.name, camera.price, camera.url)

                        mail.send_mail(
                            '%s: %s new camera(s)' % (name, cameras.count()),
                            'Filmstock\n\n%sUnsubscribe from this alert: https://filmstock.app/users/users/settings' % (message),
                            'Filmstock <alerts@mail.filmstock.app>',
                            [hunter.email],
                            fail_silently=True,
                            connection=connection,
                            html_message=html_message,
                        )

                        print('%s new cameras for %s, email sent to %s' % (cameras.count(), name, hunter.email))

                    else: print('no new cameras for %s, no email sent to %s' % (name, hunter.email))

        connection.close()
