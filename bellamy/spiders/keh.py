import scrapy
# from hunter.items import CameraItem

class kehCameraSpider(scrapy.Spider):

    name = 'keh'
    start_urls = ['https://www.keh.com/shop/cameras/film-cameras.html?stock=1',]

    def parse(self, response):
        for camera in response.css('li.product-item'):

            if camera.css('div.unavailable') is not None:

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
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
