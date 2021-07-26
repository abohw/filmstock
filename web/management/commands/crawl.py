from django.core.management.base import BaseCommand
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

class Command(BaseCommand):
      help = "Release the spiders"

      def handle(self, *args, **options):
          process = CrawlerRunner(get_project_settings())

        # film crawlers
          process.crawl('acfilm')
          process.crawl('fpp')
          process.crawl('retrospekt')
          process.crawl('brooklyn-film')
          process.crawl('precision-film')
          process.crawl('bhfilm')
          process.crawl('freestyle')
          process.crawl('moment')
          process.crawl('ultrafine')

        # camera crawlers
          process.crawl('brooklyn')
          process.crawl('austin_camera')
          process.crawl('precision')
          process.crawl('keh')
          process.crawl('bh')
        # not super impressed with etsy, tbh
        # process.crawl('etsy')

          d = process.join()
          d.addBoth(lambda _: reactor.stop())

          reactor.run()
