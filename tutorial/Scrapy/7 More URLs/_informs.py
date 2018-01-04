from scrapy import Spider
from scrapy.http import Request

class InformSpider(Spider):
    name = 'informurl'
    start_urls = (
            'http://pubsonline.informs.org/journal/orsc',
            )
    doc_prefix_url = 'http://pubsonline.informs.org'

    # change
    base_url = 'http://pubsonline.informs.org/toc/orsc/'

    def geneurl(self, v):
        return self.base_url + str(v) + '/1'

    def parse(self, response):
        url = self.geneurl(1)
        meta = {'v':1}
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
        article_xpath = './/a[@class="ref nowrap"]/@href'

        print("From: ", response.url, '------------  < --  (* _ *')
        n = 0
        for docurl in [self.doc_prefix_url + i for i in response.xpath(article_xpath).extract()]:
            n += 1
            print(docurl)
        # 1/1 --> 1/2; 1/2 --> 1/3; --- 404
        url = response.url[:-1] + str(int(response.url[-1])+1)

        if n != 0:
            yield Request(url, callback = self.parse_issue)

    def parse_document(self, response):
        pass
