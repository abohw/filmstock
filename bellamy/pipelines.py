from web.models import Camera, filmStock, Source
from django.utils import timezone
import pytz

BANNED_WORDS = [
    'dslr', 'digital', 'decorative', 'better', 'parts',
    'light meter', 'bag', 'sunglasses', 'nope',
    'shipping', 'camera lens', 'player', 'filter',
    'radio', 'passports', 'walkman', 'flashes',
    'neck strap', 'hardcover', 'reel', 'flash bar', 'expired', ]


def clean_price(param):
    return param.strip().replace('$', '').replace(',','').replace('USD','')


class BellamyPipeline:

    def process_item(self, item, spider):

        url = item['url'].split('?')[0]

        try:
            price = clean_price(item['price'])

        except Exception:
            price = None

        try:
            source = Source.objects.get(short_name__exact=item['source'])

        except Source.DoesNotExist:
            source = Source.objects.create(short_name=item['source'])

        if item['price'] is not None and item['type'] == 'camera' and not any([x in item['name'].lower() for x in BANNED_WORDS]):

            try:
                image = item['image']

            except KeyError:
                image = None

            try:
                camera = Camera.objects.get(url__exact=url)

                camera.image = image
                camera.lastSeen = timezone.now()
                camera.save()

            except Camera.DoesNotExist:

                if float(price) > 10:

                    name = item['name'].strip()

                    Camera.objects.create(
                        name = name,
                        url = url,
                        source = source,
                        store = item['store'],
                        price = price,
                        image = image,
                        createdAt = timezone.now(),
                        lastSeen = timezone.now(),
                    )

        elif item['type'] == 'film':

            try:
                film = filmStock.objects.get(url__exact=url)

                film.price = price
                film.lastSeen = timezone.now()
                film.save()

            except filmStock.DoesNotExist:

                name = item['name'].strip()

                filmStock.objects.create(
                    name = name,
                    price = price,
                    url = url,
                    source = source,
                )

        return item
