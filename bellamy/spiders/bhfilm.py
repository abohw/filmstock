import scrapy
# from hunter.items import CameraItem

class bhCameraFilmSpider(scrapy.Spider):

    name = 'bhfilm'
    start_urls = [
     'https://www.bhphotovideo.com/c/buy/35mm-film/ci/39569?filters=fct_a_filter_by%3A03_INSTOCK',
     'https://www.bhphotovideo.com/c/buy/Polaroid-Fujifilm-Instant-Film/ci/327/N/4093113315?filters=fct_a_filter_by%3A03_INSTOCK',
     'https://www.bhphotovideo.com/c/buy/120-film/ci/39570?filters=fct_a_filter_by%3A03_INSTOCK',
     'https://www.bhphotovideo.com/c/buy/Sheet-Film/ci/335/N/4093113314?filters=fct_a_filter_by%3A03_INSTOCK',
     'https://www.bhphotovideo.com/c/buy/other-film-formats/ci/39571?filters=fct_a_filter_by%3A03_INSTOCK',]

    def parse(self, response):

        for camera in response.css('div[class*=productInner]'):

            price = camera.css('span[data-selenium=uppedDecimalPriceFirst]::text').get(), camera.css('sup[data-selenium=uppedDecimalPriceSecond]::text').get()

            if price is not None:

                yield {
                'name': camera.css('span[data-selenium=miniProductPageProductName]::text').get(),
                'url': 'https://bhphotovideo.com%s' % (camera.css('a::attr(href)').get()),
                'price': '%s.%s' % (price),
                'source': 'bh',
                'store': '',
                'type': 'film',
                }

        next_page = response.css('a[data-selenium=listingPagingPageNext]::attr(href)').get()

        if next_page is not None:
            nextUrl = response.urljoin(next_page)
            yield scrapy.Request(nextUrl, callback=self.parse)
