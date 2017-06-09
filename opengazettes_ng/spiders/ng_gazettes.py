import scrapy


class GazetteSpider(scrapy.Spider):
    name = "ng_gazettes"
    allowed_domains = ["dds.crl.edu"]


    def start_requests(self):
        url = 'https://dds.crl.edu/crldelivery/27040'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass

    def check(self):
        pass

