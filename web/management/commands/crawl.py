from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class Command(BaseCommand):
      help = "Release the spiders"

      def handle(self, *args, **options):
          process = CrawlerProcess(get_project_settings())

        # film crawlers
          process.crawl('acfilm')
          process.crawl('fpp')
          process.crawl('retrospekt')
          process.crawl('brooklyn-film')
          process.crawl('precision-film')
          process.crawl('bhfilm')

        # camera crawlers
          process.crawl('brooklyn')
          process.crawl('austin_camera')
          process.crawl('precision')
          process.crawl('keh')
          process.crawl('bh')
        # not super impressed with etsy, tbh
        # process.crawl('etsy')

          process.start()
