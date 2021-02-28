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
    'https://www.etsy.com/shop/QualityCameraCompany?section_id=24648149',
    'https://www.etsy.com/shop/QualityCameraCompany?section_id=24648139',
    'https://www.etsy.com/shop/QualityCameraCompany?section_id=24648143',
    'https://www.etsy.com/shop/QualityCameraCompany?section_id=26885330',
    'https://www.etsy.com/shop/QualityCameraCompany?section_id=24648185',
    'https://www.etsy.com/shop/QualityCameraCompany?section_id=25431258',
    'https://www.etsy.com/shop/jeremiahsphotocorner',
    'https://www.etsy.com/shop/DevelopStopFix',
    'https://www.etsy.com/shop/grainyvision',
    ]

    def parse(self, response):

        store = response.css('div.shop-name-and-title-container h1::text').get()

        for camera in response.css('a.listing-link'):
            yield {
            'name': camera.css('a.listing-link::attr(title)').get(),
            'url': camera.css('a.listing-link::attr(href)').get(),
            'price': camera.css('span.currency-value::text').get(),
            'source': 'etsy',
            'store': store.lower(),
            'type': 'camera',
            }

        global page
        page += 1
        url = 'a.wt-action-group__item[data-page=\"%s\"]::attr(href)' % (page)
        next_page = response.css(url).get()

        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
