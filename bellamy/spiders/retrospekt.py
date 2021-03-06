import scrapy
from web.models import Source

itemCount = 0

class retrospektFilmSpider(scrapy.Spider):

    name = 'retrospekt'
    source = 'retrospekt'
    allowed_domains = ['retrospekt.com',]
    start_urls = [
     'https://retrospekt.com/collections/film',]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(retrospektFilmSpider, cls).from_crawler(crawler, *args, **kwargs)
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
        for camera in response.css('div.ProductItem'):
            yield {
            'name': camera.css('a::text').getall()[1],
            'url': 'https://retrospekt.com%s' % (camera.css('a::attr(href)').get()),
            'price': camera.css('span.Price::text').get(),
            'source': 'retrospekt',
            'store': '',
            'type': 'film',
            }
