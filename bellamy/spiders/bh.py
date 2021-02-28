import scrapy
# from hunter.items import CameraItem

class bhCameraSpider(scrapy.Spider):

    name = 'bh'
    start_urls = [
     'https://www.bhphotovideo.com/c/buy/Cameras/ci/3087/N/3655322819',
     'https://www.bhphotovideo.com/c/buy/35mm-Cameras/ci/3017/N/3607616145',
     'https://www.bhphotovideo.com/c/buy/General/ci/3147/N/3755784780',]

    def parse(self, response):
        for camera in response.css('div[class*=productInner]'):
            yield {
            'name': camera.css('span[data-selenium=miniProductPageProductName]::text').get(),
            'url': 'https://bhphotovideo.com%s' % (camera.css('a::attr(href)').get()),
            'price': camera.css('span[data-selenium=uppedDecimalPriceFirst]::text').get(),
            'source': 'bh',
            'store': '',
            'type': 'camera',
            }

#        next_page = response.css('ul.pagination li a::attr(href)').getall()
#        if next_page is not None:
#            try:
#                nextUrl = response.urljoin(next_page[1])
#            except:
#                nextUrl = response.urljoin(next_page[0])
#
#            yield scrapy.Request(nextUrl, callback=self.parse)
