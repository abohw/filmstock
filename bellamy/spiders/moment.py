import scrapy
# from hunter.items import CameraItem

class momentFilmSpider(scrapy.Spider):

    name = 'moment'
    start_urls = ['https://www.shopmoment.com/film?in-stock=1&sort=bestSellers',]

    def parse(self, response):

        for camera in response.css('article.product-card-display'):

            yield {
            'name': '%s %s' % (camera.css('ul.product-card-brands li a::text').get().strip(), camera.css('h2::text').get().strip()),
            'price': camera.css('div.product-card-pricing a span::text').get(),
            'url': 'https://www.shopmoment.com%s' % (camera.css('a::attr(href)').get()),
            'source': 'moment',
            'store': '',
            'type': 'film',
            }
