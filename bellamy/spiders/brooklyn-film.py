import scrapy
from scrapy_selenium import SeleniumRequest
# from hunter.items import CameraItem

class brooklynFilmCameraFilmSpider(scrapy.Spider):

    name = 'brooklyn-film'
    start_urls = ['https://www.brooklynfilmcamera.com/film',]

    def start_requests(self):

        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        for camera in response.css('a.product'):

            if not camera.css('div.sold-out'):

                yield {
                'name': camera.css('div.product-title::text').get(),
                'price': camera.css('span.sqs-money-native::text').get(),
                'url': 'https://www.brooklynfilmcamera.com%s' % (camera.css('a::attr(href)').get()),
                'source': 'brooklyn',
                'store': '',
                'type': 'film',
                }
