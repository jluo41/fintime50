from scrapy import Spider
from scrapy.http import Request


class URLSpider(Spider):
    name = 'moreurl'
    start_urls = (
            "http://www.journals.elsevier.com/decision-support-systems/",
            )
    base_url = "http://www.sciencedirect.com/science/journal/01679236/open-access"

    def parse(self, response):
        # the response is from start_urls, it is a index response
        # but we don't process it here

        url = self.base_url
        # here we want the volume urls
        # quest this url and let method parse_volume to process it.
        yield Request(url, callback =self.parse_volume1)

    def parse_volume1(self, response):
        volume_xpath1 = '//div[@id="volumeIssueData"]/ol/li/a[@class="volLink"]/@href'

        for url in ['http://www.sciencedirect.com'+ i for i in response.xpath(volume_xpath1).extract()]:
            yield Request(url, callback = self.parse_volume2)


    def parse_volume2(self, response):
        volume_xpath2 = '//div[@id="volumeIssueData"]/ol//div[@class="txt currentVolumes"]/a/@href'
        article_xpath = '//ol[@class="articleList results"]//a[@class="cLink artTitle S_C_artTitle "]/@href'

        for url in ['http://www.sciencedirect.com' + i for i in response.xpath(volume_xpath2).extract()]:
            yield Request(url, callback = self.parse_volume3)

        print("From: ", response.url,'------------  < --  (* _ *')
        for docurl in response.xpath(article_xpath).extract():
            # print(docurl) should be Request(docurl, callback = self.parse_document)
            print(docurl)

    def parse_volume3(self, response):
        article_xpath = '//ol[@class="articleList results"]//a[@class="cLink artTitle S_C_artTitle "]/@href'

        print("From: ", response.url,'------------  < --  (* _ *')
        for docurl in response.xpath(article_xpath).extract():
            print(docurl)


    def parse_document(self, response):
        # in order to spare the resource
        # in this section, this method won't be called
        pass
