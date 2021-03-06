import scrapy
# from hunter.items import CameraItem

class retrospektFilmSpider(scrapy.Spider):

    name = 'retrospekt'
    start_urls = [
     'https://retrospekt.com/collections/film',]

    def parse(self, response):
        for camera in response.css('div.ProductItem'):
            yield {
            'name': camera.css('a::text').getall()[1],
            'url': 'https://retrospekt.com%s' % (camera.css('a::attr(href)').get()),
            'price': camera.css('span.Price::text').get(),
            'source': 'retrospekt',
            'store': '',
            'type': 'film',
            }