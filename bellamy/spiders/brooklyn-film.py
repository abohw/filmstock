import scrapy
from web.models import Source

itemCount = 0

class brooklynFilmCameraFilmSpider(scrapy.Spider):

    name = 'brooklyn-film'
    source = 'brooklyn'
    allowed_domains = ['brooklynfilmcamera.com',]
    start_urls = ['https://www.brooklynfilmcamera.com/film',]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(brooklynFilmCameraFilmSpider, cls).from_crawler(crawler, *args, **kwargs)
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
        for camera in response.css('a.product'):

            if not camera.css('div.sold-out'):

                yield {
                'name': camera.css('div.product-title::text').get(),
                'price': camera.css('span.sqs-money-native::text').get(),
                'url': 'https://www.brooklynfilmcamera.com%s' % (camera.css('a::attr(href)').get()),
                'source': 'brooklyn',
                'store': '',
                'type': 'film',
                }
