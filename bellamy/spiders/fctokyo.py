import scrapy
# from hunter.items import CameraItem

page = 1

class fctSpider(scrapy.Spider):

    name = 'fct'
    start_urls = [
    'https://filmcameratokyo.com/collections/all',
    ]

    def parse(self, response):

        for camera in response.css('div.product'):

            if not camera.css('span.soldout').get():

                yield {
                'name': camera.css('a.product-block-title::text').get(),
                'url': 'https://filmcameratokyo.com%s' % (camera.css('a.img-link::attr(href)').get()),
                'price': camera.css('span.money::text').get(),
                'source': 'fct',
                'store': '',
                }

        next_page = response.css('a.next::attr(href)').get()

        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
