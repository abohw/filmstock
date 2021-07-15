import scrapy
from web.models import Source

itemCount = 0

class ultrafineFilmSpider(scrapy.Spider):

    name = 'ultrafine'
    source = 'ultrafine'
    allowed_domains = ['ultrafineonline.com',]
    start_urls = [
        'https://www.ultrafineonline.com/kodakcolorfilm.html',
        'https://www.ultrafineonline.com/fucn100coprf.html',
        'https://www.ultrafineonline.com/fuprficl35fo.html',
        'https://www.ultrafineonline.com/fuprficl120f.html',
        'https://www.ultrafineonline.com/fuslfi.html',
        'https://www.ultrafineonline.com/agvipl200cof.html',
        'https://www.ultrafineonline.com/agvi400coprf.html',
        'https://www.ultrafineonline.com/agfaslidefilm.html',
        'https://www.ultrafineonline.com/agfavista100.html',
        'https://www.ultrafineonline.com/koprfibl.html',
        'https://www.ultrafineonline.com/cicofi.html',
        'https://www.ultrafineonline.com/losofipa.html',
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ultrafineFilmSpider, cls).from_crawler(crawler, *args, **kwargs)
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
        for camera in response.css('div.fcol'):

            if not camera.css('div.add-to-cart'):

                yield {
                'name': camera.css('div.name a::text').get(),
                'price': camera.css('div.price::text').get(),
                'url': 'https://www.ultrafineonline.com/%s' % (camera.css('a::attr(href)').get()),
                'source': 'ultrafine',
                'store': '',
                'type': 'film',
                }
