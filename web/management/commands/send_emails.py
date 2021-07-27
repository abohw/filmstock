from django.core.management import BaseCommand
from django.conf import settings
from django.utils import timezone
import pytz
from django.core import mail
from hunters.models import Hunter
from web.models import Camera, emailTask
from django.template import loader
from django.db.models import Max


class Command(BaseCommand):
    help = 'what'

    def sourceCameras(self, search, lastRun):

        cameras = Camera.objects.filter(createdAt__gt=lastRun)

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

        try:
            lastRun = emailTask.objects.filter(success=True).latest('id').time
        except emailTask.DoesNotExist:
            lastRun = timezone.now() - timezone.timedelta(minutes=30)

        connection = mail.get_connection()
        connection.open()

        sent = 0
        skipped = 0

        for hunter in Hunter.objects.filter(is_subscribed=True):

            searches = hunter.searches.filter(is_subscribed=True)

            follows = hunter.follows.filter(is_subscribed=True)
            filmPriceDrops = follows.filter(film__lowUpdatedOn__gt=lastRun)
            filmInStock = follows.filter(in_stock=False).annotate(lastSeen=Max('film__stock__lastSeen'))

            if filmInStock:

                for follow in filmInStock:

                    if follow.lastSeen >= lastRun:

                        follow.in_stock = True
                        follow.save()

                        html_message = loader.render_to_string(
                            'emails/film-in-stock.html',
                            {
                                'name': 'https://filmstock.app%s' % follow.film.url,
                                'url': url,
                            }
                        )

                        mail.send_mail(
                            'Back in stock: %s %s' % (follow.film.brand, follow.film.name),
                            'Filmstock\n\nhttps://filmstock.app/film/%s/\n\nUnsubscribe from this alert: https://filmstock.app/users/users/settings' % (
                                follow.film.id),
                            'Filmstock <alerts@mail.filmstock.app>',
                            [hunter.email],
                            fail_silently=True,
                            connection=connection,
                            html_message=html_message,
                        )

                        sent += 1
                        print('film in stock for %s, email sent to %s' % (follow.film.name, hunter.email))

            if filmPriceDrops:

                for follow in filmPriceDrops:

                    html_message = loader.render_to_string(
                       'emails/new-film.html',
                       {
                           'name': '%s %s' % (follow.film.brand, follow.film.name),
                           'url': 'https://filmstock.app%s' % follow.film.url,
                           'price': follow.film.lowLast30d,
                       }
                     )

                    mail.send_mail(
                       'New low price: %s %s' % (follow.film.brand, follow.film.name),
                       'Filmstock\n\nhttps://filmstock.app/film/%s/\n\nUnsubscribe from this alert: https://filmstock.app/users/users/settings' % (follow.film.id),
                       'Filmstock <alerts@mail.filmstock.app>',
                       [hunter.email],
                       fail_silently=True,
                       connection=connection,
                       html_message=html_message,
                    )

                    sent += 1
                    print('film price drop for %s, email sent to %s' % (follow.film.name, hunter.email))

            if searches:

                for search in searches:

                    cameras = self.sourceCameras(search, lastRun)
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

                        sent += 1
                        print('%s new cameras for %s, email sent to %s' % (cameras.count(), name, hunter.email))

                    else:
                        skipped += 1

        connection.close()

        taskMax = emailTask.objects.count()

        if taskMax > 200:
            for task in emailTask.objects.all().order_by('-time')[200:taskMax]:
                task.delete()

        emailTask.objects.create(
            sent=sent,
            skipped=skipped,
            success=True,
        )
