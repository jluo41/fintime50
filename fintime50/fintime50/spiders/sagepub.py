from scrapy import Spider
from scrapy.http import Request
from fintime50.xpaths.sagepub import Xpath
from fintime50.parsers.sagepub import load_source, load_document, load_author



class SagepubSpider(Spider):
    parsed_urls = []
    doc_prefix_url = 'http://journals.sagepub.com'
    # xpath
    source = Xpath.get('source')
    document = Xpath.get('document')
    author = Xpath.get('author')
    document_url = Xpath.get('document_url')
    relationship = Xpath.get('relationship')

    def geneurl(self, v):
        return self.base_url + str(v) + '/1'

    def parse(self, response):
        # yield SourceItem()
        l = load_source(response, self.source)
        yield l.load_item()
        # get source's publication_title
        publication_title = response.xpath(self.relationship['publication_title']).extract()[0]
        # start parse Volume pages
        url = self.geneurl(1)
        meta = {'v':1, 'publication_title':publication_title}
        yield Request(url, meta = meta, callback =self.parse_volume, dont_filter = True)


    def parse_volume(self,response):
        # 1/1 --> 1/1
        url = response.url
        if url not in self.parsed_urls:
            self.parsed_urls.append(url)
        yield Request(url, meta = response.meta, callback = self.parse_issue)

        response.meta['v'] += 1
        # 1/1 --> 2/1
        url = self.geneurl(response.meta['v'])
        if url not in self.parsed_urls:
            yield Request(url, meta = response.meta, callback = self.parse_volume, dont_filter = True)

    def parse_issue(self, response):
        ## the same codes in parse_issue method
        print("From: ", response.url, '------------  < --  (* _ *')
        n = 0
        for docurl in [self.doc_prefix_url + i  for i in response.xpath(self.document_url).extract()]:
            if docurl not in self.parsed_urls:
                n += 1
                self.parsed_urls.append(docurl)
                yield Request(docurl, meta = response.meta, callback = self.parse_document)
        # 1/1 --> 1/2
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
            for l in load_author(response, self.author):
                l.add_value('doc_url', doc_url)
                yield l.load_item()
        else:
            print(" $ No Authors $   ", response.url, " <-----   LOOK HERE! ~\('o ')")

class HRSpider(SagepubSpider):
    name = 'hr'
    start_urls = (
        'https://us.sagepub.com/en-us/nam/human-relations/journal200870',
        )
    base_url = 'http://journals.sagepub.com/toc/huma/'


class OSSpider(SagepubSpider):
    name = 'os'
    start_urls = (
        'https://us.sagepub.com/en-us/nam/organization-studies/journal201657',
        )
    base_url = 'http://journals.sagepub.com/toc/ossa/'

class ASQSpdier(SagepubSpider):
    name = 'asq'
    start_urls = (
        'https://us.sagepub.com/en-us/nam/administrative-science-quarterly/journal202065',
        )
    base_url = 'http://journals.sagepub.com/toc/asqa/'

class JMSpider(SagepubSpider):
    name = 'jm'
    start_urls = (
        'https://us.sagepub.com/en-us/nam/journal-of-management/journal201724',
        )
    base_url = 'http://journals.sagepub.com/toc/joma/'
