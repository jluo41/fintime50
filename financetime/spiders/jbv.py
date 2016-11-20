# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst
from scrapy import Spider
from scrapy.http import Request
from dateutil.parser import parse
from financetime.items import DocumentItem, AuthorItem, SourceItem, KeywordItem


class JBVSpider(Spider):
    name = 'jbv'
    start_urls = (
            "http://www.journals.elsevier.com/journal-of-business-venturing/",
            )
    parsed_urls = []
    base_url = "http://www.sciencedirect.com/science/journal/08839026/"

    def getdate(self, dates):
        d = {}
        d['submission_date'] = None
        d['revision_date'] = None
        d['accepted_date'] = None
        d['online_date'] = None
        for date in dates:
            if 'Received' in date:
                d['submission_date'] = parse(date.split('Received ')[-1])
            elif 'Revised' in date:
                d['revision_date'] = parse(date.split('Revised ')[-1])
            elif 'Accepted' in date:
                d['accepted_date'] = parse(date.split('Accepted ')[-1])
            elif 'Available online' in date:
                d['online_date'] = parse(date.split('Available online ')[-1])
        return d

    def cleanhtml(self, raw_html):
      cleanr = re.compile('<.*?>')
      cleantext = re.sub(cleanr, '', raw_html)
      return cleantext


    def parse(self, response):
        self.parsed_urls.append(response.url)

        issn_xpath = '//*[@class="issn keyword"]/span/text()'
        chief_editor_xpath = '//*[@id="Title"]//span[@class="nowrap"]/text()'
        title_xpath = '//*[@id="Title"]//h1[@itemprop="name"]/text()'
        description_xpath = '//*[@class="publication-description"]//p'
        coverimage_xpath = '//*[@id="Title"]//img[@class="cover-img"]/@src'


        l = ItemLoader(item = SourceItem(), response = response)
        l.default_output_processor = TakeFirst()
        l.add_xpath("issn",issn_xpath)
        l.add_xpath('chief_editor', chief_editor_xpath)

        l.add_xpath('coverimage', coverimage_xpath)

        l.add_xpath('description', description_xpath, Join(), self.cleanhtml)
        l.add_value('home_url', response.url)

        publication_title = l.get_xpath( title_xpath)
        l.add_value('publication_title', publication_title)

        yield l.load_item()

        url = self.base_url +'1'
        meta = {'v':1, 'publication_title':publication_title}
        yield Request(url, meta = meta, callback =self.parse_volume)

    def parse_volume(self,response):
        if response.status == 200:
            self.parsed_urls.append(response.url)

            article_xpath = '//ol[@class="articleList results"]//a[@class="cLink artTitle S_C_artTitle "]/@href'


            for docurl in response.xpath(article_xpath).extract():
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
        if response.status == 200:
            ## the same codes in parse_issue method.
            article_xpath = '//ol[@class="articleList results"]//a[@class="cLink artTitle S_C_artTitle "]/@href'

            n = 0
            for docurl in response.xpath(article_xpath).extract():
                if docurl not in self.parsed_urls:
                    n +=1
                    self.parsed_urls.append(docurl)
                    yield Request(docurl, meta = response.meta, callback = self.parse_document)


            url = response.url[:-1] + str(int(response.url[-1])+1)
            if url not in self.parsed_urls and n != 0:
                self.parsed_urls.append(url)
                yield Request(url, meta= response.meta, callback = self.parse_issue)


    def parse_document(self, response):
        auths0 = response.xpath('//*[@class="author-group"]')
        auths = response.xpath('//ul[@class="authorGroup noCollab svAuthor"]/li')
        if response.status == 200 and (len(auths)!= 0 or len(auths0) != 0):

            # document xpath
            title_xpath = '//*[@class="svTitle"]/text()'
            title_xpath0 = '//*[@class="article-title"]/text()'

            abstract_xpath = '//div[@class="abstract svAbstract "]/p/text()'
            abstract_xpath0 = '//div[@class="abstract abstract-type-author"]/div/text()'

            date_xpath = '//*[@class="articleDates"]/dd/text()'
            date_xpath0 = '//*[@class="article-history-dates"]/text()'

            submission_xpath = '//*[@class="volIssue"]/a/text()'
            submission_xpath0 = '//*[@class="journal-volume"]/a/text()'

            dp_xpath = '//*[@class="volIssue"]/text()'
            dp_xpath0 = '//*[@class="journal-volume"]/text()'

            # load the document item
            l = ItemLoader(item = DocumentItem(), response = response)
            l.default_output_processor = TakeFirst()

            l.add_value('coverpage_url', response.url)
            l.add_xpath('abstract', [abstract_xpath, abstract_xpath0])
            title = l.get_xpath([title_xpath, title_xpath0])
            l.add_value('title', title)

            # add location
            submission = l.get_xpath([submission_xpath, submission_xpath0])
            l.add_value('submission_path', submission)

            # add document dates
            dates = [i for i in l.get_xpath([date_xpath,date_xpath0])[0].split(', ')]
            d = self.getdate(dates)

            l.add_value('submission_date',d['submission_date'])
            l.add_value('revision_date',d['revision_date'])
            l.add_value('accepted_date', d['accepted_date'])
            l.add_value('online_date', d['online_date'])


            date_page = l.get_xpath([dp_xpath,dp_xpath0])[0].split(', ')
            try:
                l.add_value('publication_date', parse(date_page[-2]))
            except:
                pass

            # add pages

            try:
                pages = date_page[-1].split()[-1]
                if '–' in pages:
                    fp = int(pages.split('–')[0])
                    lp = int(pages.split('–')[1])
                elif '-' in pages:
                    fp = int(pages.split('-')[0])
                    lp = int(pages.split('-')[1])
                l.add_value('fpage', fp)
                l.add_value('lpage', lp)
                l.add_value('pages', lp-fp+1)
            except:
                pass

            l.add_value('publication_title', response.meta['publication_title'])

            yield l.load_item()



            # keyword
            keyword_xpath = '//*[@class="svKeywords"]/span/text()'
            keyword_xpath0 = '//*[@class="keyword"]/text()'

            keywords = l.get_xpath([keyword_xpath,keyword_xpath0])
            for k in keywords:
                k1 = k.split(';')[0]
                l = ItemLoader(item = KeywordItem(), response = response)
                l.default_output_processor = TakeFirst()
                l.add_value('keyword', k1)
                l.add_value('title', title)
                yield l.load_item()


            # author

            # author item
            # we have defined the auths at the first line.

            for auth in auths:
                l = ItemLoader(item = AuthorItem(), response = response)
                l.default_output_processor = TakeFirst()

                fn = auth.xpath('a[@class="authorName svAuthor"]/@data-fn').extract()[0]
                ln = auth.xpath('a[@class="authorName svAuthor"]/@data-ln').extract()[0]
                l.add_value('fname', fn)
                l.add_value('lname', ln)

                try:
                    l.add_value('email', auth.xpath('a[@class="auth_mail"]/@href').extract()[0][7:])
                except:
                    pass

                try:
                    fid = auth.xpath('a[@class="intra_ref auth_aff"]/@id').extract()[0][1:]
                    address = l.get_xpath('//*[@id="%s"]/span/text()' %fid)
                    # elif i in univelist:# institution = i# break
                    for i in address[0].split(', '):
                        if "niversity" in i:
                            institution = i
                            break
                    l.add_value('address', address)
                    l.add_value('institution', institution)
                except:
                    pass

                try:
                    href = auth.xpath('span/a[@class="authorVitaeLink"]/@href').extract()[0][1:]
                    vitae = response.xpath('//p[@id="%s"]/text()' %href).extract()[0]
                    l.add_value('vitae', fn+' '+ln+vitae)
                except:
                    pass

                try:
                    href = auth.xpath('span/a[@class="authorVitaeLink"]/@href').extract()[0][1:]
                    avatar = response.xpath('//div[@id="%shidden"]//img/@src' %href).extract()[0]
                    l.add_value('avatar', avatar)
                except:
                    pass

                l.add_value('title', title)
                yield l.load_item()

            for auth in auths0:
                l = ItemLoader(item = AuthorItem(), response = response)
                l.default_output_processor = TakeFirst()
                name = auth.xpath('.//a/@data-related-url').extract()[0].split('&')[-2:]
                fn = name[-1].split('first-name=')[-1]
                ln = name[0].split('last-name=')[-1]

                l.add_value('fname', fn)
                l.add_value('lname', ln)

                try:
                    address = auth.xpath('.//*[@class="affiliation__text"]/text()').extract()
                    for i in address[0].split(', '):
                        # elif i in univelist:# institution = i# break
                        if "niversity" in i:
                            institution = i
                            break
                    l.add_value('address', address)
                    l.add_value('institution', institution)
                except:
                    pass

                try:
                    href = auth.xpath('.//*[@class="footnote-ref"]/@href').extract()
                    vitae = response.xpath('//*[@id="%s"]/dd/text()' %href[0][1:]).extract()[0]
                    l.add_value('vitae', fn+ ' ' +ln+vitae)
                except:
                    pass

                try:
                    email = auth.xpath('.//*[@class="author-email"]/@href').extract()[0][7:]
                    l.add_value('email', email)
                except:
                    pass

                l.add_value('title', title)
                yield l.load_item()


        else:
            print(" ^ No Authors ^   ", response.url, " <-----   LOOK HERE! ~\('o ')")
