import scrapy
from web.models import Source

itemCount = 0

class momentFilmSpider(scrapy.Spider):

    name = 'moment'
    source = 'moment'
    allowed_domains = ['shopmoment.com',]
    start_urls = ['https://www.shopmoment.com/film?in-stock=1&sort=bestSellers',]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(momentFilmSpider, cls).from_crawler(crawler, *args, **kwargs)
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

        for camera in response.css('article.product-card-display'):

            yield {
            'name': '%s %s' % (camera.css('ul.product-card-brands li a::text').get().strip(), camera.css('h2::text').get().strip()),
            'price': camera.css('div.product-card-pricing a span::text').get(),
            'url': 'https://www.shopmoment.com%s' % (camera.css('a::attr(href)').get()),
            'source': 'moment',
            'store': '',
            'type': 'film',
            }
