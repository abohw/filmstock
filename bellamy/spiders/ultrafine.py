import scrapy
# from hunter.items import CameraItem

class ultrafineFilmSpider(scrapy.Spider):

    name = 'ultrafine'
    start_urls = [
        'https://www.ultrafineonline.com/kodakcolorfilm.html',
        'https://www.ultrafineonline.com/fucn100coprf.html',
        'https://www.ultrafineonline.com/fuprficl35fo.html',
        'https://www.ultrafineonline.com/fuprficl120f.html',
        'https://www.ultrafineonline.com/fuslfi.html',
        'https://www.ultrafineonline.com/agvipl200cof.html',
        'https://www.ultrafineonline.com/agvi400coprf.html',
        'https://www.ultrafineonline.com/agfaslidefilm.html',
        'https://www.ultrafineonline.com/agfavista100.html',
        'https://www.ultrafineonline.com/koprfibl.html',
        'https://www.ultrafineonline.com/cicofi.html',
        'https://www.ultrafineonline.com/losofipa.html',
    ]

    def parse(self, response):
        for camera in response.css('div.fcol'):

            if not camera.css('div.add-to-cart'):

                yield {
                'name': camera.css('div.name a::text').get(),
                'price': camera.css('div.price::text').get(),
                'url': 'https://www.ultrafineonline.com/%s' % (camera.css('a::attr(href)').get()),
                'source': 'ultrafine',
                'store': '',
                'type': 'film',
                }
