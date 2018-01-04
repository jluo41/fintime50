import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst, MapCompose
from fintime50.items import DocumentItem, AuthorItem, SourceItem, KeywordItem
from dateutil.parser import parse

def load_source(response, source):
    l = ItemLoader(item = SourceItem(), response = response)
    l.default_output_processor = TakeFirst()
    l.add_xpath("issn",source['issn'])

    editor = response.xpath('//*[@id="metaData"]/p[2]/text()').extract()
    chief_editor = editor[0].split(': ')[1]
    l.add_value('chief_editor', chief_editor[:100])

    l.add_xpath('publication_title', source['publication_title'],Join())
    l.add_xpath('coverimage', source['coverimage'])
    #l.add_xpath('description', source['description'], Join(), cleanhtml)
    l.add_value('home_url', response.url)
    return l

def load_document(response, document):
    l = ItemLoader(item = DocumentItem(), response = response)
    l.default_output_processor = TakeFirst()
    l.add_value('coverpage_url', response.url)
    l.add_xpath('abstract', document['abstract'],Join())
    l.add_xpath('title', document['title'], Join())

    # need to fix
    submission = l.get_xpath(document['submission_path'])[-3].strip()
    l.add_value('submission_path', submission)

    # handle dates
    dates = [i for i in l.get_xpath(document['date'])[0].split(', ')]
    try:
        l.add_value('accepted_date', parse(dates[-1]))
        l.add_value('revision_date',parse(dates[-2]))
        l.add_value('online_date',parse(dates[-3]))
    except:
        pass

    # handle pages
    try:
        pages = submission_page[-1]
        p = pages.split()[-1].split('–',1)

        l.add_value('fpage', int(p[0]))
        l.add_value('lpage', int(p[1]))
        l.add_value('pages', int(p[1])-int(p[0])+1)
    except:
        pass

    return l


def load_author(response,author):
    auths = response.xpath(author['auth'])
    for auth in auths:
        l = ItemLoader(item = AuthorItem(), response = response)
        l.default_output_processor = TakeFirst()
        # author's first name and last name
        try:
            full = auth.xpath(author['name']).extract()[0].split()
            fn = full[0]
            ln = full[-1]
            l.add_value('fname', fn.capitalize())
            l.add_value('lname', ln.capitalize())
        except:
            pass

        # author's email
        try:
            email = auth.xpath(author['email']).extract()[0]
            l.add_value('email', email)
        except:
            pass

        # author's institution
        try:
            institution = auth.xpath('./div/ol/li/text()').extract()
            l.add_value('institution', institution, str.strip)
        except:
            pass

        yield l
