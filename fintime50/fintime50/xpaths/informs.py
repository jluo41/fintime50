source = dict(
    issn = './/div[@class="wrapped "]/div/div[@class="pb-rich-text"]/p/span/text()',
    publication_title = './/ul[@class="breadcrumbs"]/li/text()',
    description = './/div[@class="pb-rich-text"]/p',
    coverimage = './/div[@class="pb-columns row-fluid "]//div[@class="wrapped "]/div/a/img/@src'
    )

document_url = './/a[@class="ref nowrap"]/@href'

document = dict(
    title = './/h1[@class="chaptertitle"]/text()',
    abstract = './/div[@class="abstractSection abstractInFull"]/p/text()',
    submission_path = './/ul[@class="breadcrumbs"]/li/a/text()',
    revision_date = './/*[@class="publicationContentReceivedDate dates"]/text()',
    accepted_date = './/*[@class="publicationContentAcceptedDate dates"]/text()',
    online_date = './/*[@class="publicationContentEpubDate dates"]/text()',
    pages = './/div[@class="publicationContentPageRange"]/text()'
    )

author = dict(
    name = './/div[@class="contribDegrees"]/a[@class="entryAuthor"]/text()',
    institution = './/*[@class="contribAff"]/text()')


keyword = './/*[@class="abstractKeywords"]//a/text()'


Xpath = dict(
	source = source,
	document = document,
	author = author,
	keyword = keyword,
	document_url = document_url
	)
