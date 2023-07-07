import scrapy

from ..items import PepParseItem
from ..settings import DOMAIN, DOMAIN_LINK


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = DOMAIN
    start_urls = DOMAIN_LINK

    def parse(self, response):
        peps = response.css('#numerical-index table.pep-zero-table tbody tr')
        for pep in peps:
            link = pep.css('td a::attr(href)').get()
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = (response.css('h1.page-title::text').get().split(' '))

        data = {
            'number': int(title[1]),
            'name': ' '.join(title[3:]),
            'status': response.css('abbr::text').get()
        }
        yield PepParseItem(data)
