# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from web.models import Camera
from django.utils import timezone
import pytz

def clean_price(param):
    return param.strip().replace('$', '').replace(',','')

class FilmstockPipeline:
    def process_item(self, item, spider):

        if Camera.objects.filter(url__exact=item['url']).count() == 0:

            if 'dslr' not in item['name'].lower() and 'digital' not in item['name'].lower():
                price = clean_price(item['price'])
                if float(price) >= 11:

                    Camera.objects.create(
                        name = item['name'],
                        url = item['url'],
                        source = item['source'],
                        store = item['store'],
                        price = price,
                        createdAt = timezone.now(),
                        lastSeen = timezone.now(),
                    )

                    print("new camera added")

        else:
            camera = Camera.objects.get(url__exact=item['url'])

            if camera.createdAt <= (timezone.now() - timezone.timedelta(days=3)):
                print("updated, no longer new")
                camera.new = False

            else: print("updated, still new")

            camera.lastSeen = timezone.now()

            camera.save()

        return item
