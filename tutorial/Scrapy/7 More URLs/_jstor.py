from scrapy import Spider
from scrapy.http import Request


class JstorSpider(Spider):
    name = 'jstorurl'
    start_urls = (
            'https://www.jstor.org/journal/acadmanaj',
            )
    jstor_url = 'https://www.jstor.org'

    base_url = 'https://www.jstor.org/journal/acadmanaj'

    def parse(self, response):
        # parse the description of the journal
        # pass
        year = './/dl[@class="accordion"]/@data-decade'
        for url in [ self.base_url + '?decade=' + i for i in response.xpath(year).extract()]:
            yield Request(url, callback =self.parse_year)   

    def parse_year(self, response):
        issue = './/li[@data-doi]/a/@href'
        for issue_url in [self.jstor_url + i for i in response.xpath(issue).extract()]:
            yield Request(issue_url, callback = self.parse_issue)

    def parse_issue(self, response):
        print("From: ", response.url,'------------  < --  (* _ *')
        article = './/div[@class="title"]/a/@href'
        article_urls = [ self.jstor_url+ i for i in response.xpath(article).extract()]
        for article_url in article_urls:
            print(article_url)




