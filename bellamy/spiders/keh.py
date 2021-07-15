import scrapy
from web.models import Source

itemCount = 0

class kehCameraSpider(scrapy.Spider):

    name = 'keh'
    source = 'keh'
    allowed_domains = ['keh.com',]
    start_urls = ['https://www.keh.com/shop/cameras/film-cameras.html?stock=1',]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(kehCameraSpider, cls).from_crawler(crawler, *args, **kwargs)
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
        for camera in response.css('li.product-item'):

            if camera.css('div.unavailable').get() is None:

                price = camera.css('span.price::text').get()

                if price is not None:

                    yield {
                    'name': camera.css('meta[itemprop=name]::attr(content)').get(),
                    'url': camera.css('a.product-item-link::attr(href)').get(),
                    'price': price,
                    'source': 'keh',
                    'store': '',
                    'type': 'camera',
                    }

        next_page = response.css('a[id=load-more-product-link]::attr(href)').get()

        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
