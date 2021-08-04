from web.models import Source
import scrapy

itemCount = 0

class robertsCameraSpider(scrapy.Spider):

    name = 'roberts'
    source = 'roberts'
    allowed_domains = ['usedphotopro.com',]
    start_urls = [
        'https://usedphotopro.com/products/usedcameras/used-slrs/used-film-slrs',
        'https://usedphotopro.com/products/usedcameras/used-medium-format?cat=1380',
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(robertsCameraSpider, cls).from_crawler(crawler, *args, **kwargs)
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
        for camera in response.css('div.product-item-info'):

            if not camera.css('div.unavailable'):

                yield {
                'name': camera.css('a.product-item-link::text').get(),
                'url': camera.css('a.product-item-link::attr(href)').get(),
                'price': camera.css('span.price-wrapper::attr(data-price-amount)').get(),
                'image': camera.css('img.product-image-photo::attr(src)').get(),
                'source': 'roberts',
                'store': '',
                'type': 'camera',
                }

        next_page = response.css('ul.pages-items li.item a::attr(href)').getall()

        if next_page is not None:
            try:
                nextUrl = response.urljoin(next_page[0])
            except:
                pass

            yield scrapy.Request(nextUrl, callback=self.parse)
