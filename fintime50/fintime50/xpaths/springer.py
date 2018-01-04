#
source = dict(
    issn = '//span[@class="pissn"]/text()',
    publication_title = './/h1[@id="title"]/text()',
    description = './/div[@class="abstract-content formatted"]/p/text()',
    coverimage = './/img[@class="look-inside-cover"]/@src'
    )


# paper
document = dict(
    title = './/h1[@class="ArticleTitle"]/text()',
    abstract = './/p[@id="Par1"]/text()',
    online_date = './/dd[@class=/a[@class="gtm-first-online"]/text()',
    meta = './/p[@class="icon--meta-keyline-before"]/*/text()',
    publication_date = './/p[@class="icon--meta-keyline-before"]/span/time/@datetime'
    )


author = dict(
    auths = './/ul[@class="test-contributor-names"]',
    auth = './li',
    name = './/span[@class="authors-affiliations__name"]/text()',
    email = './/a[@class="gtm-email-author"]/@title',
    affil_id = './/li[@data-affiliation]/@data-affiliation',
    affiliation = './/*[@id="%s"]',
    department = './/*[@class="affiliation__department"]/text()',
    university = './/*[@class="affiliation__name"]/text()',
    city = './/*[@class="affiliation__city"]/text()',
    country = './/*[@class="affiliation__country"]/text()'
    )


keyword = './/span[@class="Keyword"]/text()'


relationship = dict(
    publication_title = './/h1[@id="title"]/text()',
    title = './/h1[@class="ArticleTitle"]/text()'
    )


issue = './/a[@class="title"]/@href'

article = './/h3//a/@href'


Xpath = dict(
    source = source,
    document = document,
    author = author,
    keyword = keyword,
    relationship = relationship,
    article = article,
    issue = issue
    )
