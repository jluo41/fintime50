from scrapy import Spider
from scrapy.http import Request
from fintime50.xpaths.springer import Xpath
from fintime50.parsers.springer import load_source, load_document, load_author, load_keyword


class SpringerSpider(Spider):

    base_url = "http://link.springer.com"

    source = Xpath.get('source')
    document = Xpath.get('document')
    keyword = Xpath.get('keyword')
    author = Xpath.get('author')
    document_url = Xpath.get('document_url')
    relationship = Xpath.get('relationship')
    issue = Xpath.get('issue')
    article = Xpath.get('article')

    def new_volume(self, v):
        return 'https://rd.springer.com/journal/10551/volume/%d/toc' %v

    def parse(self, response):
        # parse the description of the journal
        # pass
        l = load_source(response, self.source)
        yield l.load_item()
        publication_title = response.xpath(self.relationship['publication_title']).extract()
        meta = {'v':1, 'publication_title':publication_title}
        volume_url = self.new_volume(1)
        yield Request(volume_url,
                      meta = meta,
                      callback =self.parse_volume)

    def parse_volume(self,response):

        issue_urls = [self.base_url + i for i in response.xpath(self.issue).extract()]
        for issue_url in issue_urls:
            yield Request(issue_url,
                          meta = response.meta,
                          callback = self.parse_issue)

        response.meta['v'] += 1
        volume_url = self.new_volume(response.meta['v'])
        yield Request(volume_url,
                      meta= response.meta,
                      callback = self.parse_volume)

    def parse_issue(self, response):
        print("From: ", response.url,'------------  < --  (* _ *')
        article_urls = [ self.base_url + i for i in response.xpath(self.article).extract()]
        for article_url in article_urls:
            yield Request(article_url,
                          meta = response.meta,
                          callback = self.parse_document)

    def parse_document(self, response):
        auths = response.xpath(self.author['auths'])

        if len(auths.xpath(self.author['auth'])) != 0:
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


class JBESpider(SpringerSpider):
    name = 'jbe'
    start_urls = (
        'https://link.springer.com/journal/10551',
        )

class JIBSSpider(SpringerSpider):
    name = 'jibs'
    start_urls = (
        'https://link.springer.com/journal/41267',
        )

class JAMSSpider(SpringerSpider):
    name = 'jams'
    start_urls = (
        'https://link.springer.com/journal/11747',
        )

class RASSpider(SpringerSpider):
    name = 'ras'
    start_urls = (
        'https://link.springer.com/journal/11142',
        )
