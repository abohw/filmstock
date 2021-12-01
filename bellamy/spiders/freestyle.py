import scrapy
from web.models import Source

itemCount = 0
page = 1

class freestyleFilmSpider(scrapy.Spider):

    name = 'freestyle'
    source = 'freestyle'
    allowed_domains = ['freestylephoto.biz',]
    start_urls = ['https://www.freestylephoto.biz/category/1-Film?max=96',]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(freestyleFilmSpider, cls).from_crawler(crawler, *args, **kwargs)
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
        for camera in response.css('div.product-grid-top'):

            if not camera.css('div.inventory_message strong'):

                yield {
                'name': camera.css('a[itemprop=url]::text').get(),
                'url': 'https://freestylephoto.biz%s' % (camera.css('a[itemprop=url]::attr(href)').get()),
                'price': camera.css('span[itemprop=price] strong::text').get(),
                'source': 'freestyle',
                'store': '',
                'type': 'film',
                }

        next_page = response.css('div.pagination ul li a::attr(href)').getall()

        global page

        if next_page:
            nextUrl = response.urljoin(next_page[page-1])
            page += 1

            yield scrapy.Request(nextUrl, callback=self.parse)
