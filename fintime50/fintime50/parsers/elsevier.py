
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst
from fintime50.items import DocumentItem, AuthorItem, SourceItem, KeywordItem
from dateutil.parser import parse

def getdate(dates):
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


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


#############

def load_source(response, source):
    l = ItemLoader(item = SourceItem(), response = response)
    l.default_output_processor = TakeFirst()
    l.add_xpath("issn",source['issn'])
    l.add_xpath('chief_editor', source['chief_editor'])
    l.add_xpath('publication_title', source['publication_title'])
    l.add_xpath('coverimage', source['coverimage'])
    l.add_xpath('description', source['description'], Join(), cleanhtml)
    l.add_value('home_url', response.url)
    publication_title = l.get_xpath(source['publication_title'])
    return l



def load_document(response, document):
    l = ItemLoader(item = DocumentItem(), response = response)
    l.default_output_processor = TakeFirst()
    l.add_value('coverpage_url', response.url)
    l.add_xpath('abstract', document['abstract'])
    l.add_xpath('title', document['title'])
    l.add_xpath('submission_path', document['submission_path'])

    # handle dates
    dates = [i for i in l.get_xpath(document['date'])[0].split(', ')]
    d = getdate(dates)
    l.add_value('submission_date',d['submission_date'])
    l.add_value('revision_date',d['revision_date'])
    l.add_value('accepted_date', d['accepted_date'])
    l.add_value('online_date', d['online_date'])

    date_page = l.get_xpath(document['dp'])[0].split(', ')
    try:
        l.add_value('publication_date', parse(date_page[-2]))
    except:
        pass

    # handle pages
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

    # mark it down, with source's publication_title
    return l



def load_keyword(response, keyword):
    for k in response.xpath(keyword).extract():
        k1 = k.split(';')[0]
        l = ItemLoader(item = KeywordItem(), response = response)
        l.default_output_processor = TakeFirst()
        l.add_value('keyword', k1)
        yield l



def load_author(response,author):
    auths = response.xpath(author['auth'])
    for auth in auths:
        l = ItemLoader(item = AuthorItem(), response = response)
        l.default_onput_processor = TakeFirst()

        # author's first name and last name
        fn = auth.xpath(author['fn']).extract()[0]
        ln = auth.xpath(author['ln']).extract()[0]
        l.add_value('fname', fn)
        l.add_value('lname', ln)

        # author's email
        try:
            email = auth.xpath(author['email']).extract()[0][7:]
            l.add_value('email', email)
        except:
            pass

        # author's address and institution
        try:
            fid = auth.xpath(author['fid']).extract()[0][1:]
            address = l.get_xpath(author['address'] %fid)

            for i in address[0].split(', '):
                if 'niversity' in i:
                    institution = i
                    break
            l.add_value('address', address)
            l.add_value('institution', institution)
        except:
            pass

        # author's vitae
        try:
            href = auth.xpath(author['href']).extract()[0][1:]
            vitae = response.xpath(author['vitae'] %href).extract()[0]
            l.add_value('vitae', fn+' '+ln+vitae)
        except:
            pass

        # author's avatar
        try:
            href = auth.xpath(author['href']).extract()[0][1:]
            avatar = response.xpath(author['avatar'] %href).extract()[0]
            l.add_value('avatar', avatar)
        except:
            pass

        yield l




def load_author0(response, author):
    auths = response.xpath(author['auth'])
    for auth in auths:
        l = ItemLoader(item = AuthorItem(), response = response)
        l.default_output_processor = TakeFirst()

        # add author's fname and lname
        name = auth.xpath(author['name']).extract()[0].split('&')[-2:]
        fn = name[-1].split('first-name=')[-1]
        ln = name[0].split('last-name=')[-1]

        l.add_value('fname', fn)
        l.add_value('lname', ln)

        # add author's email
        try:
            email = auth.xpath(author['email']).extract()[0][7:]
            l.add_value('email', email)
        except:
            pass


        # add author's institution and address
        try:
            address = auth.xpath(author['address']).extract()
            for i in address[0].split(', '):
                # elif i in univelist:# institution = i# break
                if "niversity" in i:
                    institution = i
                    break
            l.add_value('address', address)
            l.add_value('institution', institution)
        except:
            pass

        # add author's vitae
        try:
            href = auth.xpath(author['href']).extract()
            vitae = response.xpath(author['vitae'] %href[0][1:]).extract()[0]
            l.add_value('vitae', fn+ ' ' +ln+vitae)
        except:
            pass

        yield l
