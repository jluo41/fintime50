from scrapy import Spider
from scrapy.http import Request
from fintime50.xpaths.informs import Xpath
from fintime50.parsers.informs import load_source, load_document, load_author, load_keyword

class InformsSpider(Spider):
    doc_prefix_url = 'http://pubsonline.informs.org'
    source = Xpath.get('source')
    document = Xpath.get('document')
    keyword = Xpath.get('keyword')
    author = Xpath.get('author')
    document_url = Xpath.get('document_url')

    def geneurl(self, v):
        return self.base_url + str(v) + '/1'

    def parse(self, response):
        l = load_source(response, self.source)
        yield l.load_item()
        # get source's publication_title
        publication_title = response.xpath(self.source['publication_title']).extract()[-1].replace('\n', '').strip()
        meta = {'v':1, 'publication_title':publication_title}
        url = self.geneurl(1)
        yield Request(url, meta = meta, callback =self.parse_volume, dont_filter = True)

    def parse_volume(self,response):
        # 1/1 ---> 1/1
        url = response.url
        yield Request(url, meta = response.meta, callback = self.parse_issue)

        response.meta['v'] += 1
        # 1/1 ----> 2/1
        url = self.geneurl(response.meta['v'])
        yield Request(url, meta = response.meta, callback = self.parse_volume, dont_filter = True)


    def parse_issue(self, response):

        ## the same codes in parse_issue method.
        print("From: ", response.url, '------------  < --  (* _ *')
        n = 0
        for docurl in [self.doc_prefix_url + i for i in response.xpath(self.document_url).extract()]:
            n += 1
            yield Request(docurl, meta = response.meta, callback = self.parse_document)
        # 1/1 --> 1/2; 1/2 --> 1/3; --- 404
        url = response.url[:-1] + str(int(response.url[-1])+1)

        if n != 0:
            yield Request(url, meta = response.meta, callback = self.parse_issue)

    def parse_document(self, response):
        if len(response.xpath(self.author['name'])) != 0:
            l = load_document(response, self.document)
            l.add_value('publication_title', response.meta['publication_title'])
            yield l.load_item()

            doc_url = response.url

            for l in load_author(response, self.author):
                l.add_value('doc_url', doc_url)
                yield l.load_item()

            for l in load_keyword(response, self.keyword):
                l.add_value('doc_url', doc_url)
                yield l.load_item()
        else:
            print(" $ No Authors $   ", response.url, " <-----   LOOK HERE! ~\('o ')")


class ORSCSpider(InformsSpider):
    """ Orgranization Science """
    name = 'orsc'
    start_urls = (
            'http://pubsonline.informs.org/journal/orsc',
            )
    base_url = 'http://pubsonline.informs.org/toc/orsc/'


class ISRSpider(InformsSpider):
    """ Information Systems Research """
    name = 'isr'
    start_urls = (
            'http://pubsonline.informs.org/journal/isre',
            )
    base_url = 'http://pubsonline.informs.org/toc/isre/'

class MSSpider(InformsSpider):
    """ Management Science """
    name = 'ms'
    start_urls = (
            'http://pubsonline.informs.org/journal/mnsc',
            )
    base_url = 'http://pubsonline.informs.org/toc/mnsc/'

class MSOMSpider(InformsSpider):
    """ Manufuacturing and Service Operations Management """
    name = 'msom'
    start_urls = (
            'http://pubsonline.informs.org/journal/msom',
            )
    base_url = 'http://pubsonline.informs.org/toc/msom/'

class MKTSSpider(InformsSpider):
    """ Marketing Science """
    name = 'mkts'
    start_urls = (
            'http://pubsonline.informs.org/journal/mksc',
            )
    base_url = 'http://pubsonline.informs.org/toc/mksc/'

class OPRSpider(InformsSpider):
    """ Operations Research """
    name = 'opr'
    start_urls = (
            'http://pubsonline.informs.org/journal/opre',
            )
    base_url = 'http://pubsonline.informs.org/toc/opre/'
