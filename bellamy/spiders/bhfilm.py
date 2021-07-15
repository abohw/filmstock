import scrapy
from web.models import Source

itemCount = 0

class bhCameraFilmSpider(scrapy.Spider):

    name = 'bhfilm'
    source = 'bh'
    allowed_domains = ['bhphotovideo.com',]
    start_urls = [
     'https://www.bhphotovideo.com/c/buy/35mm-film/ci/39569?filters=fct_a_filter_by%3A03_INSTOCK',
     'https://www.bhphotovideo.com/c/buy/Polaroid-Fujifilm-Instant-Film/ci/327/N/4093113315?filters=fct_a_filter_by%3A03_INSTOCK',
     'https://www.bhphotovideo.com/c/buy/120-film/ci/39570?filters=fct_a_filter_by%3A03_INSTOCK',
     'https://www.bhphotovideo.com/c/buy/Sheet-Film/ci/335/N/4093113314?filters=fct_a_filter_by%3A03_INSTOCK',
     'https://www.bhphotovideo.com/c/buy/other-film-formats/ci/39571?filters=fct_a_filter_by%3A03_INSTOCK',]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(bhCameraFilmSpider, cls).from_crawler(crawler, *args, **kwargs)
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

        for camera in response.css('div[class*=productInner]'):

            dollars = camera.css('span[data-selenium=uppedDecimalPriceFirst]::text').get()
            cents = camera.css('sup[data-selenium=uppedDecimalPriceSecond]::text').get()

            if dollars is not None and cents is not None:

                yield {
                'name': camera.css('span[data-selenium=miniProductPageProductName]::text').get(),
                'url': 'https://bhphotovideo.com%s' % (camera.css('a::attr(href)').get()),
                'price': '%s.%s' % (dollars, cents),
                'source': 'bh',
                'store': '',
                'type': 'film',
                }

        next_page = response.css('a[data-selenium=listingPagingPageNext]::attr(href)').get()

        if next_page is not None:
            nextUrl = response.urljoin(next_page)
            yield scrapy.Request(nextUrl, callback=self.parse)
