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

class BellamyPipeline:
    def process_item(self, item, spider):

        url = item['url'].split('?')[0]

        if Camera.objects.filter(url__exact=url).count() == 0:

            BANNED_WORDS = ['dslr', 'digital', 'decorative', 'light meter']

            if any([x in item['name'].lower() for x in BANNED_WORDS]):

                print("skipping, name contains banned word")

            else:

                price = clean_price(item['price'])
                if float(price) >= 11:

                    Camera.objects.create(
                        name = item['name'],
                        url = url,
                        source = item['source'],
                        store = item['store'],
                        price = price,
                        createdAt = timezone.now(),
                        lastSeen = timezone.now(),
                    )

                    print("new camera added")

        else:
            camera = Camera.objects.get(url__exact=url)
            camera.lastSeen = timezone.now()
            camera.save()

        return item
