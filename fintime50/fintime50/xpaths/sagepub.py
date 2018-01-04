
# home items xpath
source = dict(
    issn = '//span[@class="margin-right"]/text()',
    chief_editor = '//td[@class="journal-contributor-member"]/a/text()',
    publication_title = './/h1[@class="heading-large heading-spacing--small"]/text()',
    description = './/div[@class="field field-name-field-website-configuration field-type-text-long field-label-hidden"]',
    coverimage = './/img[@class="sage-thumbnail-width-150px lazy"]/@data-original'
    )

document_url = './/a[@class="ref nowrap"]/@href'

document = dict(
    title = './/div[@class="publicationContentTitle"]/h1/text()',
    abstract = './/div[@class="abstractSection abstractInFull"]/p/text()',
    submission_path = './/div[@class="articleJournalNavTitle"]/text()',
    pages = './/div[@class="Article information"]/div/text()',
    dates = './/div[@class="published-dates"]/text()'
    )

author =dict(
    auth = './/div[@class="contribDegrees"]',
    name = './/a[@class="entryAuthor"]/text()',
    email = './/a[@class="email"]/@href',
    institution = './/div[@class="artice-info-affiliation"]/text()'
    )

relationship = dict(
    publication_title = './/h1[@class="heading-large heading-spacing--small"]/text()',
    title = './/div[@class="publicationContentTitle"]/h1/text()'
    )

Xpath = dict(
	source = source,
	document = document,
	author = author,
	relationship = relationship,
	document_url = document_url
	)
