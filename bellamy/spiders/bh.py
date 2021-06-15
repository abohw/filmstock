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

            price = camera.css('span[data-selenium=uppedDecimalPriceFirst]::text').get(), camera.css(
                'sup[data-selenium=uppedDecimalPriceSecond]::text').get()

            if price is not None:
                yield {
                    'name': camera.css('span[data-selenium=miniProductPageProductName]::text').get(),
                    'url': 'https://bhphotovideo.com%s' % (camera.css('a::attr(href)').get()),
                    'price': '%s.%s' % (price),
                    'source': 'bh',
                    'store': '',
                    'type': 'camera',
                }


        next_page = response.css('a[data-selenium=listingPagingPageNext]::attr(href)').get()

        if next_page is not None:
            nextUrl = response.urljoin(next_page)
            yield scrapy.Request(nextUrl, callback=self.parse)
