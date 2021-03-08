import scrapy
# from hunter.items import CameraItem

page = 1

class freestyleFilmSpider(scrapy.Spider):

    name = 'freestyle'
    start_urls = ['https://www.freestylephoto.biz/category/1-Film?max=96',]

    def parse(self, response):
        for camera in response.css('div.product-grid-top'):

            if not camera.css('div.inventory_message strong'):

                yield {
                'name': camera.css('a[itemprop=url]::text').get(),
                'url': 'https://freestylephoto.biz%s' % (camera.css('a[itemprop=url]::attr(href)').get()),
                'price': camera.css('span[itemprop=price] strong::text').get(),
                'source': 'freestyle',
                'store': '',
                'type': 'film',
                }

        next_page = response.css('div.pagination ul li a::attr(href)').getall()

        global page

        if next_page is not None:
            nextUrl = response.urljoin(next_page[page-1])
            page += 1

            yield scrapy.Request(nextUrl, callback=self.parse)
