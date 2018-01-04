# Wiley

# home items xpath
source = dict (
	issn = '//*[@id="issn"]/text()',
	chief_editor = '//*[@id="metaData"]/p[2]/text()',
	publication_title = '//*[@id="productTitle"]/text()',
	coverimage = '//*[@class="imgShadow"]/img/@src'
	)


volume = '//*[@class="issuesInYear closed"]/@href'

issue_url = '//*[@class="issue"]//a/@href'

# article url xpath
document_url = '//ol[@class="articles"]/li/div[@class="citation tocArticle"]/a/@href'

# -------------------
# article fields xpaths
document = dict(
	title = '//*[@class="article-header__title"]/text()',
	abstract = '//*[@class="article-section__content mainAbstract"]/p[1]/text()',
	date = '//*[@class="article-info__publication-history-data"]/text()',
	submission_path = '//*[@class="issue-header__description"]/text()',
	)

# no keyword

# author fields xpaths

# within an author selector

author = dict(
	auth = '//*[@class="article-header__authors-item"]',
	name = './@data-author-name',
	email = './div/ul/li/p/a/text()',
	institution = './div/ol/li/text()'
	)


relationship = dict(
	publication_title = '//*[@id="productTitle"]/text()',
	title = '//*[@class="article-header__title"]/text()',
	)


Xpath = dict(
    source = source,
    volumne = volume,
    document = document,
    author = author,
    relationship = relationship,
    document_url = document_url,
    issue_url = issue_url
    )
