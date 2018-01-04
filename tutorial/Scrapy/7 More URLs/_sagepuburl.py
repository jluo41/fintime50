from scrapy import Spider
from scrapy.http import Request

class URLSpider(Spider):
    name = 'moreurl'
    start_urls = (
            "https://us.sagepub.com/en-us/nam/human-relations/journal200870",
            )
    base_url = "http://journals.sagepub.com/toc/huma/"
    parsed_urls = []

    def geneurl(self, v):
        return self.base_url + str(v) + '/1'

    def parse(self, response):
        url = self.geneurl(1)
        meta = {'v':1}
        yield Request(url, meta = meta, callback =self.parse_volume, dont_filter = True)

    def parse_volume(self,response):
        # 1/1 ---> 1/1
        url = response.url
        if url not in self.parsed_urls:
            self.parsed_urls.append(url)
        yield Request(url, meta = response.meta, callback = self.parse_issue)

        response.meta['v'] += 1
        # 1/1 ----> 2/1
        url = self.geneurl(response.meta['v'])
        if url not in self.parsed_urls:
            yield Request(url, meta = response.meta, callback = self.parse_volume, dont_filter = True)


    def parse_issue(self, response):

        ## the same codes in parse_issue method.
        article_xpath = './/a[@class="ref nowrap"]/@href'

        print("From: ", response.url, '------------  < --  (* _ *')
        n = 0
        for docurl in response.xpath(article_xpath).extract():
            if docurl not in self.parsed_urls:
                n += 1
                self.parsed_urls.append(docurl)
                print(docurl)
        # 1/1 --> 1/2; 1/2 --> 1/3; --- 404
        url = response.url[:-1] + str(int(response.url[-1])+1)
        if url not in self.parsed_urls and n != 0:
            self.parsed_urls.append(url)
            yield Request(url, callback = self.parse_issue)

    def parse_document(self, response):
        pass
