# -*- coding: utf-8 -*-

# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Spider
from scrapy.http import Request
from fintime50.xpaths.elsevier import Xpath
from fintime50.parsers.elsevier import load_source, load_document, load_keyword, load_author, load_author0

class ElsevierSpider(Spider):

    source = Xpath['source']
    document = Xpath['document']
    keyword = Xpath['keyword']
    author = Xpath['author']
    document0 = Xpath['document0']
    keyword0 = Xpath['keyword0']
    author0 = Xpath['author0']
    document_url = Xpath['document_url']
    relationship = Xpath['relationship']

    def parse(self, response):
        # yield SourceItem()
        l = load_source(response, self.source)
        yield l.load_item()
        # get source's publication_title
        publication_title = response.xpath(self.relationship['publication_title']).extract()
        # start parse Volume pages
        url = self.base_url + '1'
        meta = {'v':1, 'publication_title':publication_title}
        yield Request(url, meta = meta, callback =self.parse_volume)

    def parse_volume(self,response):
        self.parsed_urls.append(response.url)
        for docurl in response.xpath(self.document_url).extract():
            if docurl not in self.parsed_urls:
                self.parsed_urls.append(docurl)
                yield Request(docurl, meta = response.meta, callback = self.parse_document)
        url = response.url + '/1'
        if url not in self.parsed_urls:
            self.parsed_urls.append(url)
            yield Request(url, meta = response.meta, callback = self.parse_issue)
        response.meta['v'] += 1
        url = self.base_url + str(response.meta['v'])
        if url not in self.parsed_urls:
            self.parsed_urls.append(url)
            yield Request(url, meta= response.meta, callback = self.parse_volume)

    def parse_issue(self, response):
        ## the same codes in parse_issue method
        n = 0
        for docurl in response.xpath(self.document_url).extract():
            if docurl not in self.parsed_urls:
                n +=1
                self.parsed_urls.append(docurl)
                yield Request(docurl, meta = response.meta, callback = self.parse_document)
        url = response.url[:-1] + str(int(response.url[-1])+1)
        if url not in self.parsed_urls and n != 0:
            self.parsed_urls.append(url)
            yield Request(url, meta= response.meta, callback = self.parse_issue)

    def parse_document(self, response):
        if len(response.xpath(self.author['auth'])) != 0:
            l = load_document(response, self.document)
            l.add_value('publication_title', response.meta['publication_title'])
            yield l.load_item()

            doc_url = response.url
            for l in load_keyword(response, self.keyword):
                l.add_value('doc_url', doc_url)
                yield l.load_item()
            for l in load_author(response, self.author):
                l.add_value('doc_url', doc_url)
                yield l.load_item()

        elif len(response.xpath(self.author0['auth'])) != 0:
            l = load_document(response, self.document0)
            l.add_value('publication_title', response.meta['publication_title'])
            yield l.load_item()
            
            doc_url = response.url
            for l in load_keyword(response, self.keyword0):
                l.add_value('doc_url', doc_url)
                yield l.load_item()
            for l in load_author0(response, self.author0):
                l.add_value('doc_url', doc_url)
                yield l.load_item()
        else:
            print(" $ No Authors $   ", response.url, " <-----   LOOK HERE! ~\('o ')")

class AOSSpider(ElsevierSpider):
    name = 'aos'
    start_urls = (
            "http://www.journals.elsevier.com/accounting-organizations-and-society/",
            )
    base_url = "http://www.sciencedirect.com/science/journal/03613682/"


class DSSSpider(ElsevierSpider):
    name = 'dss'
    start_urls = (
            "http://www.journals.elsevier.com/decision-support-systems/",
            )
    base_url = "http://www.sciencedirect.com/science/journal/01679236/"


class JAESpider(ElsevierSpider):
    name = 'jae'
    start_urls = (
            "http://www.journals.elsevier.com/journal-of-accounting-and-economics/",
            )
    base_url = "http://www.sciencedirect.com/science/journal/01654101/"


class JBVSpider(ElsevierSpider):
    name = 'jbv'
    start_urls = (
            "http://www.journals.elsevier.com/journal-of-business-venturing/",
            )
    base_url = "http://www.sciencedirect.com/science/journal/08839026/"


class JCPSpider(ElsevierSpider):
    name = 'jcp'
    start_urls = (
            "http://www.journals.elsevier.com/journal-of-consumer-psychology/",
            )
    base_url = "http://www.sciencedirect.com/science/journal/10577408/"


class JFESpider(ElsevierSpider):
    name = 'jfe'
    start_urls = (
            "http://www.journals.elsevier.com/journal-of-financial-economics/",
            )
    base_url = "http://www.sciencedirect.com/science/journal/0304405X/"


class JOMSpider(ElsevierSpider):
    name = 'jom'
    start_urls = (
            "http://www.journals.elsevier.com/journal-of-operations-management/",
            )
    base_url = "http://www.sciencedirect.com/science/journal/02726963/"


class PBHDPSpider(ElsevierSpider):
    name = 'pbhdp'
    start_urls = (
            "http://www.journals.elsevier.com/organizational-behavior-and-human-decision-processes/",
            )
    base_url = "http://www.sciencedirect.com/science/journal/07495978/"



class RPSpider(ElsevierSpider):
    name = 'rp'
    start_urls = (
            "http://www.journals.elsevier.com/research-policy/",
            )
    base_url = "http://www.sciencedirect.com/science/journal/00487333/"
