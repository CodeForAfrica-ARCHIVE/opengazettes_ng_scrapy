import json
from datetime import datetime

import dateparser as dateparser
import re
import scrapy
from scrapy import FormRequest

from opengazettes_ng.items import OpengazettesNgItem
from opengazettes_ng.pdf_reader import parse_pdf


class GazetteSpider(scrapy.Spider):
    name = "ng_gazettes"
    allowed_domains = ["dds.crl.edu"]

    def start_requests(self):
        # Get the year to be crawled from the arguments
        # The year is passed like this: scrapy crawl gazettes -a year=2017
        # Default to current year if year not passed in
        try:
            year = self.year
        except AttributeError:
            year = datetime.now().strftime('%Y')
        url = 'https://dds.crl.edu/item/json'
        form_data = {'year': str(year), 'TitleLink': str(27040)}
        yield FormRequest(url, callback=self.parse, formdata=form_data)

    def parse(self, response):
        gazettes_data = json.loads(response.body)
        for date, gazettes in gazettes_data.items():
            for gazette in gazettes:
                item = OpengazettesNgItem()
                item = self.create_meta(gazette, item, date)
                yield item

    def create_meta(self, gazette, item, date):
        link_base_url = 'https://dds.crl.edu/page/downloadall/'
        gazette_id = gazette.get('iid')
        gazette_link = link_base_url + gazette_id
        vol, no = self.build_meta(gazette_link)
        date = dateparser.parse(date)
        item['gazette_link'] = gazette_link
        item['publication_date'] = date
        item['gazette_number'] = no
        item['gazette_volume'] = vol
        item['special_issue'] = self.check_special_issue(gazette)
        item['file_urls'] = [gazette_link]
        item['filename'] = self.create_filename(gazette, vol, no, date)
        item['gazette_title'] = self.create_title(gazette, vol, no, date)
        return item

    @staticmethod
    def check_special_issue(gazette):
        if "supplement" in gazette.get('text').lower():
            return True
        return False

    @staticmethod
    def build_meta(gazette_link):
        return parse_pdf(gazette_link)

    @staticmethod
    def get_special_name(gazette):
        name = re.search("(supplement \w)", gazette.get('text'), re.IGNORECASE)
        if name:
            return name.group()
        return ''

    def create_filename(self, gazette, vol, no, date):
        return 'opengazettes-ng-vol-%s-no-%s %s-dated-%s-%s-%s' % \
            (vol, no, self.get_special_name(gazette),
             date.strftime("%d"),
             date.strftime("%B"),
             date.strftime("%Y"))

    def create_title(self, gazette, vol, no, date):
        return 'Nigeria Government Gazette Vol %s No %s %s Dated %s %s %s' % \
               (vol, no, self.get_special_name(gazette),
                date.strftime("%d"),
                date.strftime("%B"),
                date.strftime("%Y"))
