import scrapy
from scrapy_selenium import SeleniumRequest
# from hunter.items import CameraItem

class fppFilmSpider(scrapy.Spider):

    name = 'fpp'
    start_urls = [
    'http://filmphotographystore.com/collections/all/120-film',
    'http://filmphotographystore.com/collections/all/35mm-film',
    ]

    def start_requests(self):

        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

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

            yield SeleniumRequest(url=nextUrl, callback=self.parse)
