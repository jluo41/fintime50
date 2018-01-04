import re
from fintime50.items import DocumentItem, AuthorItem, SourceItem, KeywordItem
from dateutil.parser import parse
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def _get_descrip(key, response, source):
    ''' Inner Function '''
    print("run the function _get_descrip")
    
    try:
        a = response.xpath(source[key])[0].extract()
        b = cleanhtml(a).replace('  ','').replace("&amp", '')
    except:
        b=''
    value = b.replace('\n','')
    return value

def load_source(response, source):
    l = ItemLoader(item = SourceItem(), response = response)
    l.default_output_processor = TakeFirst()
    l.add_xpath("issn", source['issn'])
    l.add_xpath('publication_title', source['publication_title'])
    description = " ".join([ _get_descrip(j, response, source) for j in ['description', 'subjects', 'collections']])
    l.add_value('description', description)
    l.add_value('home_url', response.url)
    return l

def load_document(response, document):
    l = ItemLoader(item = DocumentItem(), response = response)
    l.default_output_processor = TakeFirst()

    l.add_value('coverpage_url', response.url)
    l.add_xpath('abstract', document['abstract'])
    l.add_value('title', response.xpath(document['title']).extract()[0].replace('\n', '').strip())
    meta = re.split('[()]', response.xpath(document['meta']).extract()[0].replace('\n', '').strip())
    try:
        l.add_value('submission_path', meta[0][:90])
    except:
        pass

    try:
        l.add_value('publication_date', parse(meta[1]))
    except:
        pass

    # handle pages
    try:
        pages = [ int(i) for i in meta[-1].split('pp.')[-1].split('-')]
        fp = pages[0]
        lp = pages[-1]
        l.add_value('fpage', fp)
        l.add_value('lpage', lp)
        l.add_value('pages', lp-fp+1)
    except:
        pass

    # mark it down, with source's publication_title
    return l

def load_author(response, author):
    string = response.xpath(author['names']).extract()[0].replace('\n', '').strip()
    names = [str.strip(i) for i in string.replace(' and ', ', ').split(',')]
    for name in names:
        l = ItemLoader(item = AuthorItem(), response = response)
        l.default_output_processor = TakeFirst()
        # author's first name and last name
        flname = name.split()
        fn = flname[0]
        ln = flname[-1]
        l.add_value('fname', fn)
        l.add_value('lname', ln)
        yield l

def load_keyword(response, keyword):
    keywords = response.xpath(keyword).extract()
    for k in keywords:
        l = ItemLoader(item = KeywordItem(), response = response)
        l.default_output_processor = TakeFirst()
        l.add_value('keyword', k)
        yield l
