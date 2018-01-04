# Elsevier

# home items xpath
source = dict(
    issn = '//*[@class="issn keyword"]/span/text()',
    chief_editor = '//*[@id="Title"]//span[@class="nowrap"]/text()',
    publication_title = '//*[@id="Title"]//h1[@itemprop="name"]/text()',
    description = '//*[@class="publication-description"]//p',
    coverimage = '//*[@id="Title"]//img[@class="cover-img"]/@src'
    )

# article url xpath
document_url = '//ol[@class="articleList results"]//a[@class="cLink artTitle S_C_artTitle "]/@href'


# -------------------
# article fields xpaths
document = dict(
    title = '//*[@class="svTitle"]/text()',
    abstract = '//div[@class="abstract svAbstract "]/p/text()',
    date = '//*[@class="articleDates"]/dd/text()',
    submission_path = '//*[@class="volIssue"]/a/text()',
    dp = '//*[@class="volIssue"]/text()'
    )

# keyword field xpaths
keyword = '//*[@class="svKeywords"]/span/text()'

# author fields xpaths

# within an author selector

# version 1:
author = dict(
    auth = '//ul[@class="authorGroup noCollab svAuthor"]/li',
    fn = 'a[@class="authorName svAuthor"]/@data-fn',
    ln = 'a[@class="authorName svAuthor"]/@data-ln',
    email = 'a[@class="auth_mail"]/@href',
    fid = 'a[@class="intra_ref auth_aff"]/@id',
    address = '//*[@id="%s"]/span/text()',
    href = 'span/a[@class="authorVitaeLink"]/@href',
    vitae = '//p[@id="%s"]/text()',
    avatar = '//div[@id="%shidden"]//img/@src'
    )



# ----------------


document0 = dict(
    title = '//*[@class="article-title"]/text()',
    abstract = '//div[@class="abstract abstract-type-author"]/div/text()',
    date = '//*[@class="article-history-dates"]/text()',
    submission_path = '//*[@class="journal-volume"]/a/text()',
    dp = '//*[@class="journal-volume"]/text()'
    )


keyword0 = '//*[@class="keyword"]/text()'

# author fields xpaths

# within an author selector

# version 0:
author0 = dict(
    auth = '//*[@class="author-group"]',
    name = './/a/@data-related-url',
    address = './/*[@class="affiliation__text"]/text()',
    href = './/*[@class="footnote-ref"]/@href',
    vitae = '//*[@id="%s"]/dd/text()',
    email = './/*[@class="author-email"]/@href'
    )

relationship = dict(
    publication_title = '//*[@id="Title"]//h1[@itemprop="name"]/text()',
    title = '//*[@class="svTitle"]/text()',
    title0 = '//*[@class="article-title"]/text()'
    )


Xpath = dict(
    source = source,
    document = document,
    author = author,
    keyword = keyword,
    document0 = document0,
    author0 = author0,
    keyword0 = keyword0,
    relationship = relationship,
    document_url = document_url
    )
