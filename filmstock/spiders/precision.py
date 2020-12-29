import scrapy
# from hunter.items import CameraItem

class precisionCameraSpider(scrapy.Spider):

    name = 'precision'
    start_urls = ['https://www.precision-camera.com/used/film',]

    def parse(self, response):
        for camera in response.css('div.card-body'):
            yield {
            'name': camera.css('a::text').get(),
            'url': camera.css('a::attr(href)').get(),
            'price': camera.css('span.price--withoutTax::text').get(),
            'source': 'precision',
            }
