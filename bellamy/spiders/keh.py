import scrapy
from scrapy_selenium import SeleniumRequest
# from hunter.items import CameraItem

class kehCameraSpider(scrapy.Spider):

    name = 'keh'
    start_urls = ['https://www.keh.com/shop/cameras/film-cameras.html?stock=1',]

    def start_requests(self):

        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        for camera in response.css('li.product-item'):

            price = camera.css('span.price::text').get()

            if price is not None:

                yield {
                'name': camera.css('meta[itemprop=name]::attr(content)').get(),
                'url': camera.css('a.product-item-link::attr(href)').get(),
                'price': price,
                'source': 'keh',
                'store': '',
                'type': 'camera',
                }

        next_page = response.css('a[id=load-more-product-link]::attr(href)').get()

        if next_page is not None:
            yield SeleniumRequest(url=response.urljoin(next_page), callback=self.parse)
