source = dict(
    issn = '//div[@class="issn mtm"]/text()',
    publication_title = './/div[@class="journal lookslikeh2 drop-content-title"]/text()',
    description = './/div[@class="journal_description mtm"]',
    subjects = './/div[@class="subjects mtm"]',
    collections = './/div[@class="collections mtm"]',
    coverimage = './/img[@class="cover"]/@src'
    )

document = dict(
    title = './/h1[@class="title"]/text()',
    # submission_path, publication_date, page
    meta = './/*[@class="src mbl"]/text()',
    abstract = './/*[@class="abstract1"]/text()'
    )


keyword = './/*[@class="topics mtl"]/a/text()'

author = dict(names = './/*[@class="contrib"]/text()')


year_url = './/dl[@class="accordion"]/@data-decade'

document_url = './/div[@class="media-body media-object-section main-section"]/a/@href'

issue_url = './/li[@data-doi]/a/@href'

relationship = './/h1[@class="journal-name langMatch"]/text()'

Xpath = dict(
    source = source,
    document = document,
    author = author,
    keyword = keyword,
    document_url = document_url,
    issue_url = issue_url,
    year_url = year_url,
    relationship = relationship
    )
