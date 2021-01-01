import scrapy
# from hunter.items import CameraItem

class austinCameraSpider(scrapy.Spider):

    name = 'austin_camera'
    start_urls = ['https://austincamera.com/collections/film-cameras',]

    def parse(self, response):
        for camera in response.css('div.product-card'):
            yield {
            'name': camera.css('div.product-card__title::text').get(),
            'url': 'https://austincamera.com%s' % (camera.css('a::attr(href)').get()),
            'price': camera.css('span.price-item::text').get(),
            'source': 'austin_camera',
            'store': '',
            }

        next_page = response.css('ul.pagination li a::attr(href)').getall()
        if next_page is not None:
            try:
                nextUrl = response.urljoin(next_page[1])
            except:
                nextUrl = response.urljoin(next_page[0])

            yield scrapy.Request(nextUrl, callback=self.parse)
