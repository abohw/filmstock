# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from web.models import Camera
from datetime import datetime, date, timedelta

def clean_price(param):
    return param.strip().replace('$', '').replace(',','')

class FilmstockPipeline:
    def process_item(self, item, spider):

        if Camera.objects.filter(url__exact=item['url']).count() == 0:

            if 'dslr' not in item['name'].lower() and 'digital' not in item['name'].lower():
                price = clean_price(item['price'])
                if float(price) >= 100:

                    Camera.objects.create(
                        name = item['name'],
                        url = item['url'],
                        source = item['source'],
                        store = item['store'],
                        price = price,
                        createdAt = datetime.now().strftime('%Y-%m-%d'),
                        lastSeen = datetime.now().strftime('%Y-%m-%d'),
                    )

                    print("new camera added")

        else:
            camera = Camera.objects.get(url__exact=item['url'])

            if camera.createdAt <= (date.today() - timedelta(days=7)):
                print("updated, no longer new")
                camera.new = False

            else: print("updated, still new")

            camera.lastSeen = datetime.now().strftime('%Y-%m-%d')

            camera.save()

        return item
