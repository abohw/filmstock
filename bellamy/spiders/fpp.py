import scrapy
from web.models import Source

itemCount = 0

class fppFilmSpider(scrapy.Spider):

    name = 'fpp'
    source = 'fpp'
    allowed_domains = ['filmphotographystore.com',]
    start_urls = [
    'http://filmphotographystore.com/collections/all/120-film',
    'http://filmphotographystore.com/collections/all/35mm-film',
    'https://filmphotographystore.com/collections/all/instant-film',
    'https://filmphotographystore.com/collections/all/110-film',
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(fppFilmSpider, cls).from_crawler(crawler, *args, **kwargs)
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
        for camera in response.css('a.product-grid-item'):

            if not camera.css('span.badge-label::text'):

                yield {
                'name': camera.css('p::text').get(),
                'url': 'https://filmphotographystore.com%s' % (camera.css('a.product-grid-item::attr(href)').get()),
                'price': camera.css('span.visually-hidden::text')[1].get(),
                'source': 'fpp',
                'type': 'film',
                }

        next_page = response.css('ul.pagination-custom li a::attr(href)').getall()
        if next_page is not None:
            try:
                nextUrl = response.urljoin(next_page[1])
            except:
                nextUrl = response.urljoin(next_page[0])

            yield scrapy.Request(nextUrl, callback=self.parse)
