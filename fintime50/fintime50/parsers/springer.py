from dateutil.parser import parse
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst
from fintime50.items import DocumentItem, AuthorItem, SourceItem, KeywordItem
from unicodedata import normalize



def load_source(response, source):
    l = ItemLoader(item = SourceItem(), response = response)
    l.default_output_processor = TakeFirst()
    l.add_xpath("issn", source['issn'])
    l.add_xpath('publication_title', source['publication_title'])
    l.add_xpath('coverimage', source['coverimage'])
    l.add_xpath('description',source['description'], Join() )
    l.add_value('home_url', response.url)
    publication_title = l.get_xpath(source['publication_title'])
    return l

def load_document(response, document):
    l = ItemLoader(item = DocumentItem(), response = response)
    l.default_output_processor = TakeFirst()

    l.add_value('coverpage_url', response.url)
    l.add_xpath('abstract', document['abstract'])
    l.add_xpath('title', document['title'])
    try:
        meta = l.get_xpath(document['meta'])
        l.add_value('submission_path', normalize('NFKD', meta[1] + meta[2]))
        pages = meta[-1].split(' ')[-1]
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

    l.add_value('publication_date', parse(response.xpath(document['publication_date']).extract()[0]))

    # mark it down, with source's publication_title
    return l


def load_author(response, author):
    auths = response.xpath(author['auths'])[-1]
    for auth in auths.xpath(author['auth']):
        l = ItemLoader(item = AuthorItem(), response = response)
        l.default_output_processor = TakeFirst()

        # author's first name and last name
        try:
            name = normalize('NFKD', auth.xpath(author['name']).extract()[0])
            fn = name.split()[0]
            ln = name.split()[-1]
            l.add_value('fname', fn)
            l.add_value('lname', ln)
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
            affil_id = auth.xpath(author['affil_id']).extract()[0][1:]
            affiliation = response.xpath(author['affiliation'] %(affil_id))[0]
            # department
            department = affiliation.xpath(author['department']).extract()[0]
            # university
            university = affiliation.xpath(author['university']).extract()[0]
            institution = department +' ' +  university
            l.add_value('institution', institution)

            # address
            city = affiliation.xpath(author['city']).extract()[0]
            country = affiliation.xpath(author['country']).extract()[0]
            address = city + ' ' +  country
            l.add_value('address', address)

        except:
            pass

        yield l

def load_keyword(response, keyword):
    keywords = [ normalize('NFKD', i)  for i in response.xpath(keyword).extract()]
    for k in keywords:
        l = ItemLoader(item = KeywordItem(), response = response)
        l.default_output_processor = TakeFirst()
        l.add_value('keyword', k)
        yield l
