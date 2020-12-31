from django.core.management import BaseCommand
from django.conf import settings
from datetime import date, timedelta
from django.core import mail
from hunters.models import Hunter
from web.models import Camera
from django.template import loader


class Command(BaseCommand):
    help = 'what'

    def sourceCameras(self, search):

        cameras = Camera.objects.filter(createdAt__range=[date.today() - timedelta(days=1), date.today()])

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
            if hunter.searches.all():

                for search in hunter.searches.all():

                    cameras = self.sourceCameras(search)

                    html_message = loader.render_to_string(
                        'email-alerts.html',
                        {
                            'name': search.name,
                            'cameras': cameras,
                        }
                    )

                    message = ''
                    for camera in cameras:
                        message += '%s (%s)\n%s\n\n' % (camera.name, camera.price, camera.url)

                    mail.send_mail(
                        'Yo, you got new cameras for %s' % (search.name),
                        'Hello.\n\n%s\n\nYour best friend,\nFilmstock' % (message),
                        'alerts@filmstock.app',
                        [hunter.email],
                        fail_silently=True,
                        connection=connection,
                        html_message=html_message,
                    )

        connection.close()
