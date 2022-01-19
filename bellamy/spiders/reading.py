from web.models import Source
import scrapy

itemCount = 0

class retroReadingFilmSpider(scrapy.Spider):

    name = 'reading'
    source = 'retro_reading'
    allowed_domains = ['retrophotoreading.com',]
    start_urls = [
        'https://retrophotoreading.com/collections/alpa-camera',
        'https://retrophotoreading.com/collections/bronica-camera',
        'https://retrophotoreading.com/collections/canon-camera',
        'https://retrophotoreading.com/collections/contax/Contax',
        'https://retrophotoreading.com/collections/hasselblad-camera',
        'https://retrophotoreading.com/collections/konica-cameras',
        'https://retrophotoreading.com/collections/leica-camera',
        'https://retrophotoreading.com/collections/mamiya-camera',
        'https://retrophotoreading.com/collections/minolta-camera',
        'https://retrophotoreading.com/collections/nikon-camera',
        'https://retrophotoreading.com/collections/pentax-camera',
        'https://retrophotoreading.com/collections/point-shoots',
        'https://retrophotoreading.com/collections/rollei-camera',
        'https://retrophotoreading.com/collections/voigtlander-camera',
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(retroReadingFilmSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.item_scraped, signal=scrapy.signals.item_scraped)
        crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
        return spider

    def item_scraped(self, spider):
        global itemCount
        itemCount += 1

    def spider_closed(self, spider):

        try:
            source = Source.objects.get(short_name__exact=spider.source)
            source.lastScrapeTotal = itemCount
            source.save()

        except Source.DoesNotExist:
            pass

    def parse(self, response):

        for camera in response.css('div.grid-item div.grid-item'):

            if not camera.css('div.badge--sold-out'):

                image = camera.css('img::attr(src)')

                if image:
                    image = 'https:%s' % (camera.css('img::attr(src)').get())

                else:
                    image = None

                yield {
                'name': camera.css('p::text').get(),
                'url': 'https://retrophotoreading.com%s' % (camera.css('a::attr(href)').get()),
                'price': camera.css('small::text').get(),
                'image': image,
                'source': 'retro_reading',
                'store': '',
                'type': 'camera',
                }

