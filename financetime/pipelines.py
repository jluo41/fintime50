# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm import sessionmaker
from financetime.items import DocumentItem, KeywordItem, SourceItem, AuthorItem
from financetime.models import Document, Author, Keyword, Source, sdb_connect, create_table
import os



class FinancetimePipeline(object):
    '''
    def __init__(self):
        engine = sdb_connect(os.getcwd())
        create_table(engine)
        Session = sessionmaker(bind = engine)
        self.session = Session()
    '''

    def process_item(self, item, spider):
        '''
        if isinstance(item, SourceItem):
            source = self.session.query(Source).filter_by(publication_title = item['publication_title']).first()
            if source == None:
                source = Source(**item)

                try:
                    self.session.add(source)
                except:
                    self.session.rollback()
                    raise

        elif isinstance(item, DocumentItem):

            source = self.session.query(Source).filter_by(publication_title = item['publication_title']).first()
            del item['publication_title']

            document = self.session.query(Document).filter_by(title = item['title']).first()
            if document == None:
                document = Document(**item)

                # Here is an issue, needing tests.
                try:
                    self.session.add(document)
                except:
                    self.session.rollback()
                    raise

            if source != None:
                source.documents.append(document)

        elif isinstance(item, KeywordItem):

            document = self.session.query(Document).filter_by(title = item['title']).first()
            del item['title']

            keyword = self.session.query(Keyword).filter_by(keyword = item['keyword']).first()
            if keyword == None:
                keyword = Keyword(**item)

                try:
                    self.session.add(keyword)
                except:
                    self.session.rollback()
                    raise

            if document != None:
                document.keywords.append(keyword)

        elif isinstance(item, AuthorItem):

            document = self.session.query(Document).filter_by(title = item['title']).first()
            del item['title']

            author = self.session.query(Author).filter_by(fname = item.get('fname'), lname=item.get('lname'), institution =item.get('institution'), avatar = item.get('avatar'), email=item.get('email'), vitae = item.get('vitae'), address = item.get("address")).first()
            if author == None:
                author = Author(**item)

                try:
                    self.session.add(author)
                except:
                    self.session.rollback()
                    raise
            if document != None:
                document.authors.append(author)

        self.session.commit()
        '''
        return item
