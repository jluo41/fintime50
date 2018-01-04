from scrapy import Spider
from scrapy.http import Request
from fintime50.xpaths.wiley import Xpath
from fintime50.parsers.wiley import load_source, load_document, load_author
from datetime import datetime

class WileySpider(Spider):
    # xpaths
    source = Xpath['source']
    document = Xpath['document']
    author = Xpath['author']
    issue_url = Xpath['issue_url']
    document_url = Xpath['document_url']
    relationship = Xpath['relationship']

    def parse(self, response):
        l = load_source(response, self.source)
        yield l.load_item()
        publication_title = response.xpath(self.relationship['publication_title']).extract()
        meta = dict(year = self.year, publication_title = publication_title)
        url = self.year_url %(meta['year'])
        yield Request(url, meta = meta, callback =self.parse_volume)

    def parse_volume(self,response):
        if response.status == 200:
            # the response is the year response,
            # from year get the year issues.
            for issue in response.xpath(self.issue_url).extract():
                url = self.base_url + issue
                yield Request(url, meta = response.meta, callback = self.parse_issue)
            # from year 1 to year 2
            if response.meta['year'] < datetime.now().year:
                response.meta['year'] += 1
                url = self.year_url %(response.meta['year'])
                yield Request(url, meta = response.meta, callback =self.parse_volume)

    def parse_issue(self, response):
        if response.status == 200:
            n = 0
            for docurl in response.xpath(self.document_url).extract():
                n += 1
                url = self.base_url+docurl
                self.parsed_urls.append(url)
                yield Request(url, meta = response.meta, callback = self.parse_document)

    def parse_document(self, response):
        if len(response.xpath(self.author['auth'])) != 0:
            l = load_document(response, self.document)
            l.add_value('publication_title', response.meta['publication_title'])
            yield l.load_item()
            # get author
            doc_url = response.url
            for l in load_author(response, self.author):
                l.add_value('doc_url', doc_url)
                yield l.load_item()
        else:
            print(" $ No Authors $   ", response.url, " <-----   LOOK HERE! ~\('o ')")


class CarSpider(WileySpider):
    name = 'car'
    start_urls = (
            "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1911-3846",
            )
    parsed_urls = []
    year_url = "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1911-3846/issues/fragment?activeYear=%d&SKIP_DECORATION=true"
    base_url = "http://onlinelibrary.wiley.com/"
    year = 1984


class ETPSpider(WileySpider):
    name = 'etp'
    start_urls = (
            "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1540-6520",
            )
    parsed_urls = []
    year_url = "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1540-6520/issues/fragment?activeYear=%d&SKIP_DECORATION=true"
    base_url = "http://onlinelibrary.wiley.com/"
    year = 2002


class HRMSpider(WileySpider):
    name = 'hrm'
    start_urls = (
            "http://onlinelibrary.wiley.com/journal/10.1002/(ISSN)1099-050X",
            )
    parsed_urls = []
    year_url = "http://onlinelibrary.wiley.com/journal/10.1002/(ISSN)1099-050X/issues/fragment?activeYear=%d&SKIP_DECORATION=true"
    base_url = "http://onlinelibrary.wiley.com/"
    year = 1961

class JAPSpider(WileySpider):
    name = 'jap'
    start_urls = (
            "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1559-1816",
            )
    parsed_urls = []
    year_url = "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1559-1816/issues/fragment?activeYear=%d&SKIP_DECORATION=true"
    base_url = "http://onlinelibrary.wiley.com/"
    year = 1971

class JARSpider(WileySpider):
    name = 'jar'
    start_urls = (
            "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1475-679X",
            )
    parsed_urls = []
    year_url = "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1475-679X/issues/fragment?activeYear=%d&SKIP_DECORATION=true"
    base_url = "http://onlinelibrary.wiley.com/"
    year = 2001


class JFSpider(WileySpider):
    name = 'jf'
    start_urls = (
            "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1540-6261",
            )
    parsed_urls = []
    year_url = "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1540-6261/issues/fragment?activeYear=%d&SKIP_DECORATION=true"
    base_url = "http://onlinelibrary.wiley.com/"
    year = 1946

class JMSSpider(WileySpider):
    name = 'jms'
    start_urls = (
            "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1467-6486",
            )
    parsed_urls = []
    year_url = "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1467-6486/issues/fragment?activeYear=%d&SKIP_DECORATION=true"
    base_url = "http://onlinelibrary.wiley.com/"
    year = 1964

class POMSpider(WileySpider):
    name = 'pom'
    start_urls = (
            "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1937-5956",
            )
    parsed_urls = []
    year_url = "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1937-5956/issues/fragment?activeYear=%d&SKIP_DECORATION=true"
    base_url = "http://onlinelibrary.wiley.com/"
    year = 1992

class SEJSpider(WileySpider):
    name = 'sej'
    start_urls = (
            "http://onlinelibrary.wiley.com/journal/10.1002/(ISSN)1932-443X",
            )
    parsed_urls = []
    year_url = "http://onlinelibrary.wiley.com/journal/10.1002/(ISSN)1932-443X/issues/fragment?activeYear=%d&SKIP_DECORATION=true"
    base_url = "http://onlinelibrary.wiley.com/"
    year = 2007

class SMJSpider(WileySpider):
    name = 'smj'
    start_urls = (
            "http://onlinelibrary.wiley.com/journal/10.1002/(ISSN)1097-0266",
            )
    parsed_urls = []
    year_url = "http://onlinelibrary.wiley.com/journal/10.1002/(ISSN)1097-0266/issues/fragment?activeYear=%d&SKIP_DECORATION=true"
    base_url = "http://onlinelibrary.wiley.com/"
    year = 1980


class EcoSpider(WileySpider):
    '''Econometrica'''
    name = 'eco'
    start_urls = (
            'http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1468-0262',
            )
    parsed_urls = []
    year_url = "http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1468-0262/issues/fragment?activeYear=%d&SKIP_DECORATION=true"
    base_url = "http://onlinelibrary.wiley.com/"
    year = 1999
