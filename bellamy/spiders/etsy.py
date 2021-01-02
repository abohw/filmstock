import scrapy
# from hunter.items import CameraItem

page = 1

class etsySpider(scrapy.Spider):

    name = 'etsy'
    start_urls = [
    'https://www.etsy.com/shop/SantaRosaCamera',
    'https://www.etsy.com/shop/JohnsonCamera',
    'https://www.etsy.com/shop/MyCameraCloset',
    'https://www.etsy.com/shop/KmcamerasUS',
    'https://www.etsy.com/shop/AnalogRelics',
    ]

    def parse(self, response):

        store = response.css('h1.mb-lg-1::text').get()

        for camera in response.css('a.listing-link'):
            yield {
            'name': camera.css('a.listing-link::attr(title)').get(),
            'url': camera.css('a.listing-link::attr(href)').get(),
            'price': camera.css('span.currency-value::text').get(),
            'source': 'etsy',
            'store': store.lower(),
            }

        global page
        page += 1
        url = 'a.wt-action-group__item[data-page=\"%s\"]::attr(href)' % (page)
        next_page = response.css(url).get()

        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)