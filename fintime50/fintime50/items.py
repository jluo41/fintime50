# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DocumentItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    abstract = Field()

    publication_date = Field()
    submission_date = Field()
    online_date = Field()
    revision_date = Field()
    accepted_date = Field()

    title = Field()
    coverpage_url = Field()
    fpage = Field()
    lpage = Field()
    pages = Field()
    submission_path = Field()

    publication_title = Field()


class KeywordItem(Item):
    keyword = Field()

    doc_url = Field()


class SourceItem(Item):
    publication_title = Field()
    chief_editor = Field()
    issn = Field()
    description = Field()
    home_url = Field()
    coverimage = Field()

    doc_url = Field()

class AuthorItem(Item):
    institution = Field()
    email = Field()
    avatar = Field()
    vitae = Field()
    fname = Field()
    lname = Field()
    address = Field()

    doc_url = Field()
