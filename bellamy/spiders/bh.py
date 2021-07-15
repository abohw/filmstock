from web.models import Source
import scrapy

itemCount = 0

class bhCameraSpider(scrapy.Spider):

    name = 'bh'
    source = 'bh'
    allowed_domains = ['bhphotovideo.com',]
    start_urls = [
     'https://www.bhphotovideo.com/c/buy/Cameras/ci/3087/N/3655322819',
     'https://www.bhphotovideo.com/c/buy/35mm-Cameras/ci/3017/N/3607616145',
     'https://www.bhphotovideo.com/c/buy/General/ci/3147/N/3755784780',]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(bhCameraSpider, cls).from_crawler(crawler, *args, **kwargs)
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
                    'type': 'camera',
                }

        next_page = response.css('a[data-selenium=listingPagingPageNext]::attr(href)').get()

        if next_page is not None:
            nextUrl = response.urljoin(next_page)
            yield scrapy.Request(nextUrl, callback=self.parse)
