import scrapy
from scrapy_selenium import SeleniumRequest
# from hunter.items import CameraItem

class austinCameraSpider(scrapy.Spider):

    name = 'austin_camera'
    start_urls = ['https://austincamera.com/collections/film-cameras',]

    def start_requests(self):

        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        for camera in response.css('div.product-card'):

            if not camera.css('dl.price--sold-out'):

                yield {
                'name': camera.css('div.product-card__title::text').get(),
                'url': 'https://austincamera.com%s' % (camera.css('a::attr(href)').get()),
                'price': camera.css('span.price-item::text').get(),
                'source': 'austin_camera',
                'store': '',
                'type': 'camera',
                }

        next_page = response.css('ul.pagination li a::attr(href)').getall()
        if next_page is not None:
            try:
                nextUrl = response.urljoin(next_page[1])
            except:
                nextUrl = response.urljoin(next_page[0])

            yield SeleniumRequest(url=nextUrl, callback=self.parse)
