from web.models import Source
import scrapy

itemCount = 0

class austinCameraFilmSpider(scrapy.Spider):

    name = 'acfilm'
    source = 'austin_camera'
    allowed_domains = ['austincamera.com',]
    start_urls = [
    'https://austincamera.com/collections/film-1/120',
    'https://austincamera.com/collections/film-1/35mm',
    'https://austincamera.com/collections/film-1/Instant-Film',
    'https://austincamera.com/collections/film-1/110',
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(austinCameraFilmSpider, cls).from_crawler(crawler, *args, **kwargs)
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

        for camera in response.css('div.product-card'):

            if not camera.css('dl.price--sold-out'):

                yield {
                'name': camera.css('div.product-card__title::text').get(),
                'url': 'https://austincamera.com%s' % (camera.css('a::attr(href)').get()),
                'price': camera.css('span.price-item::text').get(),
                'source': 'austin_camera',
                'type': 'film',
                }

        next_page = response.css('ul.pagination li a::attr(href)').getall()
        if next_page is not None:
            try:
                nextUrl = response.urljoin(next_page[1])
            except:
                nextUrl = response.urljoin(next_page[0])

            yield scrapy.Request(nextUrl, callback=self.parse)
