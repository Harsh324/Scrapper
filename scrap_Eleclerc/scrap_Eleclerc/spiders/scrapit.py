import scrapy


class ScrapitSpider(scrapy.Spider):
    name = 'scrapit'

    start_urls = ['https://www.e.leclerc/cat/sport-loisirs']

    def parse(self, response):
        pass
