from dateutil.parser import parse
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst
import re
import unicodedata
from fintime50.items import DocumentItem, AuthorItem, SourceItem, KeywordItem

# this function is used to strip the html tags
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def load_source(response, source):
    informs_url = "http://pubsonline.informs.org"
    coverimage = informs_url + response.xpath(source['coverimage']).extract()[-1]
    publication_title = response.xpath(source['publication_title']).extract()[-1].replace('\n', '').strip()
    issn = [i for i in response.xpath(source['issn']).extract() if "ISSN: " in i][0].replace('ISSN: ', '')
    description = unicodedata.normalize("NFKD", cleanhtml(response.xpath(source['description']).extract()[1]))

    l = ItemLoader(item = SourceItem(), response = response)
    l.default_output_processor = TakeFirst()
    l.add_value("issn", issn[:29])
    l.add_value('publication_title', publication_title)
    l.add_value('coverimage', coverimage)
    l.add_value('description', description)
    l.add_value('home_url', response.url)
    return l


def load_document(response, document):
    l = ItemLoader(item = DocumentItem(), response = response)
    l.default_output_processor = TakeFirst()
    l.add_value('coverpage_url', response.url)

    l.add_value('title', l.get_xpath(document['title'])[0].replace('\n', '').strip())
    l.add_value('submission_path', l.get_xpath(document['submission_path'])[-1].replace('\n', '').strip())

    try:
        l.add_value('abstract', l.get_xpath(document['abstract'])[0])
    except:
        pass
    # dates
    try:
        l.add_value('online_date', parse(l.get_xpath(document['online_date'])[0].replace('\n', '').strip().split('Published Online: ')[-1]))
    except:
        pass

    try:
        l.add_value('accepted_date', parse(l.get_xpath(document['accepted_date'])[0].replace('\n', '').strip().split('Accepted: ')[-1]))
    except:
        pass

    try:
        l.add_value('revision_date', parse(l.get_xpath(document['revision_date'])[0].replace('\n', '').strip().split('Received: ')[-1]))
    except:
        pass

    # handle pages
    try:
        pages = l.get_xpath(document['pages'])[0].split('\n')[-2].strip().split(' - ')
        fp = int(pages[0])
        lp = int(pages[-1])
        l.add_value('fpage', fp)
        l.add_value('lpage', lp)
        l.add_value('pages', lp-fp+1)
    except:
        pass

    # mark it down, with source's publication_title
    return l


def load_author(response, author):
    names = response.xpath(author['name']).extract()
    institutions = response.xpath(author['institution']).extract()
    for i in range(len(names)):
        name = names[i].split()
        fn = name[0]
        ln = name[-1]
        try:
            institution = institutions[i]
        except:
            institution = ''
        l = ItemLoader(item = AuthorItem(), response = response)
        l.default_output_processor = TakeFirst()
        l.add_value('fname', fn)
        l.add_value('lname', ln)
        l.add_value('institution', institution)
        yield l


def load_keyword(response, keyword):
    keywords = response.xpath(keyword).extract()
    for k in keywords:
        l = ItemLoader(item = KeywordItem(), response = response)
        l.default_output_processor = TakeFirst()
        l.add_value('keyword', k)
        yield l
