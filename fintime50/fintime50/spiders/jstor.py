from scrapy import Spider
from scrapy.http import Request

from fintime50.xpaths.jstor import Xpath
from fintime50.parsers.jstor import load_source, load_document, load_author, load_keyword


class JstorSpider(Spider):

    jstor_url = 'https://www.jstor.org'

    source = Xpath.get('source')
    document = Xpath.get('document')
    keyword = Xpath.get('keyword')
    author = Xpath.get('author')
    document_url = Xpath.get('document_url')
    issue_url = Xpath.get('issue_url')
    year_url = Xpath.get('year_url')
    relationship = Xpath.get('relationship')

    def parse(self, response):
        # parse the description of the journal
        # pass

        # coverimage is too loog to put in the database, so abondan it here /LUO
        coverimage = None

        try:
            coverimage = response.xpath(self.source['coverimage']).extract()[0]
        except:
            pass

        meta = {}

        try:
            meta['coverimage'] = coverimage[:240]
        except:
            pass

        url = response.url + '?item_view=journal_info'
        yield Request(url, meta = meta, callback = self.parse_source)

        publication_title = response.xpath(self.relationship).extract()[0]
        meta = {}
        meta['publication_title'] = publication_title
        for url in [ self.base_url + '?decade=' + i for i in response.xpath(self.year_url).extract()]:
            yield Request(url, meta = meta, callback =self.parse_year)

    def parse_source(self, response):
        l = load_source(response, self.source)
        l.add_value('coverimage', response.meta.get('coverimage'))
        yield l.load_item()


    def parse_year(self, response):
        for issue_url in [self.jstor_url + i for i in response.xpath(self.issue_url).extract()]:
            yield Request(issue_url, meta = response.meta, callback = self.parse_issue)

    def parse_issue(self, response):
        print("From: ", response.url,'------------  < --  (* _ *')
        article_urls = [ self.jstor_url+ i for i in response.xpath(self.document_url).extract()]
        for article_url in article_urls:
            print(article_url)
            yield Request(article_url, meta = response.meta, callback = self.parse_document)

    def parse_document(self, response):
        if len(response.xpath(self.author['names'])) != 0:
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


class AMJSpider(JstorSpider):
    ''' Academy of Management Journal'''
    name = 'amj'
    start_urls = (
            'https://www.jstor.org/journal/acadmanaj',
            )
    base_url = 'https://www.jstor.org/journal/acadmanaj'


class AMRSpider(JstorSpider):
    ''' Academy of Management Review'''
    name = 'amr'
    start_urls = (
            'https://www.jstor.org/journal/acadmanarevi',
            )
    base_url = 'https://www.jstor.org/journal/acadmanarevi'


class AERSpider(JstorSpider):
    ''' American Economic Review'''
    name = 'aer'
    start_urls = (
            'https://www.jstor.org/journal/amereconrevi',
            )
    base_url = 'https://www.jstor.org/journal/amereconrevi'


class JCRSpider(JstorSpider):
    ''' Journal of Consumer Research'''
    name = 'jcr'
    start_urls = (
            'https://www.jstor.org/journal/jconsrese',
            )
    base_url = 'https://www.jstor.org/journal/jconsrese'



class JFQASpider(JstorSpider):
    ''' Journal of Financial and Quantitative Analysis'''
    name = 'jfqa'
    start_urls = (
            'https://www.jstor.org/journal/jfinaquananal',
            )
    base_url = 'https://www.jstor.org/journal/jfinaquananal'



class JMISSpider(JstorSpider):
    ''' Journal of Management and Information System'''
    name = 'jmis'
    start_urls = (
            'https://www.jstor.org/journal/jmanainfosyst',
            )
    base_url = 'https://www.jstor.org/journal/jmanainfosyst'



class JMSpider(JstorSpider):
    ''' Journal of Marketing'''
    name = 'jmkt'
    start_urls = (
            'https://www.jstor.org/journal/jmarketing',
            )
    base_url = 'https://www.jstor.org/journal/jmarketing'



class JMRSpider(JstorSpider):
    ''' Journal of Marketing Research'''
    name = 'jmr'
    start_urls = (
            'http://www.jstor.org/journal/jmarkrese',
            )
    base_url = 'http://www.jstor.org/journal/jmarkrese'



class JPESpider(JstorSpider):
    ''' Journal of Political Research'''
    name = 'jpe'
    start_urls = (
            'http://www.jstor.org/journal/jpoliecon',
            )
    base_url = 'http://www.jstor.org/journal/jpoliecon'



class QJESpider(JstorSpider):
    '''Quarterly Journal of Economics'''
    name = 'qje'
    start_urls = (
            'https://www.jstor.org/journal/quarjecon',
            )
    base_url = 'https://www.jstor.org/journal/quarjecon'



class RFSSpider(JstorSpider):
    '''Review of Financial Studies'''
    name = 'rfs'
    start_urls = (
            'https://www.jstor.org/journal/revifinastud',
            )
    base_url = 'https://www.jstor.org/journal/revifinastud'




class ARSpider(JstorSpider):
    '''The Accounting Review'''
    name = 'ar'
    start_urls = (
            'https://www.jstor.org/journal/accountingreview',
            )
    base_url = 'https://www.jstor.org/journal/accountingreview'




class RESSpider(JstorSpider):
    '''The Review of Economic Studies'''
    name = 'res'
    start_urls = (
            'https://www.jstor.org/journal/revieconstud',
            )
    base_url = 'https://www.jstor.org/journal/revieconstud'
