from dateutil.parser import parse
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst, Join
from fintime50.items import DocumentItem, AuthorItem, SourceItem, KeywordItem
import re

# this function is used to strip the html tags
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def load_source(response, source):
    website_url = 'https://us.sagepub.com' 
    l = ItemLoader(item = SourceItem(), response = response)
    l.default_output_processor = TakeFirst()
    l.add_value("issn", response.xpath(source['issn']).extract()[1].split()[-1])
    l.add_value('chief_editor', response.xpath(source['chief_editor']).extract()[0])
    l.add_xpath('publication_title', source['publication_title'])
    l.add_value('coverimage', website_url + l.get_xpath(source['coverimage'])[0])
    l.add_xpath('description', './/div[@class="field-item even"]', Join(), cleanhtml, lambda x: x.replace('\n', '').replace('  ', '').strip())
    l.add_value('home_url', response.url)
    publication_title = l.get_xpath(source['publication_title'])
    return l

def load_document(response, document):
    l = ItemLoader(item = DocumentItem(), response = response)
    l.default_output_processor = TakeFirst()
    
    l.add_value('coverpage_url', response.url)
    l.add_xpath('abstract', document['abstract'])
    l.add_value('title', (l.get_xpath(document['title'])[0]).replace('\n', '').strip())
    l.add_value('submission_path', l.get_xpath(document['submission_path'])[0].replace('\n', '').strip())

    # handle dates
    try:
        dates =[i.replace('\n', '').replace(';', '').strip() for i in response.xpath(document['dates']).extract()[-2:]]
        d = [parse(i) for i in dates]
        l.add_value('online_date', d[0])
        l.add_value('publication_date', d[1])
    except:
        pass

    # handle pages
    try:
        pages = response.xpath(document['pages']).extract()[0].strip().split('\n')[-1].strip().split(':')[-1]
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

    # mark it down, with source's publication_title
    return l


def load_author(response,author):
    auths = response.xpath(author['auth'])
    for auth in auths:
        l = ItemLoader(item = AuthorItem(), response = response)
        l.default_output_processor = TakeFirst()

        # author's first name and last name
        name = auth.xpath(author['name']).extract()[0].split()
        fn = name[0]
        ln = name[-1]
        l.add_value('fname', fn)
        l.add_value('lname', ln)

        # author's email
        try:
            email = auth.xpath(author['email']).extract()[0][7:]
            l.add_value('email', email)
        except:
            pass

        # author's institution
        try:
            institution = auth.xpath(author['institution']).extract()[0]
            l.add_value('institution', institution)
        except:
            pass
        yield l


