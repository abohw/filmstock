import scrapy
from scrapy_selenium import SeleniumRequest
# from hunter.items import CameraItem

class precisionCameraSpider(scrapy.Spider):

    name = 'precision'
    start_urls = ['https://www.precision-camera.com/used/film',]

    def start_requests(self):

        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        for camera in response.css('div.card-body'):
            yield {
            'name': camera.css('a::text').get(),
            'url': camera.css('a::attr(href)').get(),
            'price': camera.css('span.price--withoutTax::text').get(),
            'source': 'precision',
            'store': '',
            'type': 'camera',
            }
