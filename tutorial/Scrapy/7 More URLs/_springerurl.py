from scrapy import Spider
from scrapy.http import Request


class SpringerSpider(Spider):
    name = 'springerurl'
    start_urls = (
            "http://link.springer.com/journal/volumesAndIssues/41267",
            )
    base_url = "http://link.springer.com"

    def new_volume(self, v):
        return 'https://rd.springer.com/journal/10551/volume/%d/toc' %v

    def parse(self, response):
        # parse the description of the journal
        # pass
        meta = {'v':1}
        volume_url = self.new_volume(1)
        yield Request(volume_url,
                      meta = meta,
                      callback =self.parse_volume)

    def parse_volume(self,response):

        issue = './/a[@class="title"]/@href'
        issue_urls = [self.base_url + i for i in response.xpath(issue).extract()]
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
        article = './/h3//a/@href'
        article_urls = [ self.base_url + i for i in response.xpath(article).extract()]
        for article_url in article_urls:
            print(article_url)
