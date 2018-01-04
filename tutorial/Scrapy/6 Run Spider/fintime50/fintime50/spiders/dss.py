# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst
from scrapy import Spider
from dateutil.parser import parse
from fintime50.items import SourceItem


class DSSSpider(Spider):
    name = 'dss'
    start_urls = (
                  "http://www.journals.elsevier.com/decision-support-systems/",
                  )
    base_url = "http://www.sciencedirect.com/science/journal/01679236/"


    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext


    def parse(self, response):
        issn_xpath = '//*[@class="issn keyword"]/span/text()'
        chief_editor_xpath = '//*[@id="Title"]//span[@class="nowrap"]/text()'
        title_xpath = '//*[@id="Title"]//h1[@itemprop="name"]/text()'
        description_xpath = '//*[@class="publication-description"]//p'
        coverimage_xpath = '//*[@id="Title"]//img[@class="cover-img"]/@src'

        l = ItemLoader(item = SourceItem(), response = response)
        l.default_output_processor = TakeFirst()
        l.add_xpath("issn",issn_xpath)
        l.add_xpath('chief_editor', chief_editor_xpath)
        l.add_xpath('coverimage', coverimage_xpath)
        l.add_xpath('description', description_xpath, Join(), self.cleanhtml)
        l.add_value('home_url', response.url)
        publication_title = l.get_xpath( title_xpath)
        l.add_value('publication_title', publication_title)

        yield l.load_item()
