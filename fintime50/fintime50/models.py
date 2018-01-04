# to get the database's absolute path.
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# for building the basic mapping table classes.
from sqlalchemy import Column, String, Integer, Table, Text, DateTime

# for building relationships among tables.
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship



# create_engine need database URI as the augument.
# sqlite3's URI form (for Mac) is such: 'sqlite:////absolute/path/to/database'

def sdb_connect(basedir, name = 'data'):
    return create_engine('sqlite:///'+os.path.join(basedir, name + '.sqlite'))

def mdb_connect():
    MySQL_DB = 'mysql+pymysql://root:@localhost:3306/fintime50?charset=utf8'
    return create_engine(MySQL_DB)

# we get Base from the initializaiton of class declarative_base
# Base will be the basic table which will be extended to other tables
# then we connect this basic table to the engine.

Base = declarative_base()


def create_table(engine):
    Base.metadata.create_all(engine)


# construct register table
documents_authors = Table('documents_authors', Base.metadata,
                          Column('documents_id', ForeignKey("documents.id"), primary_key=True),
                          Column('authors_id', ForeignKey("authors.id"), primary_key=True))

documents_keywords = Table("documents_keywords",Base.metadata,
                           Column("documents_id", ForeignKey("documents.id"),primary_key=True),
                           Column("keywords_id", ForeignKey('keywords.id'), primary_key=True))

documents_fields = Table('documents_fields', Base.metadata,
                         Column('documents_id', ForeignKey('documents.id'),primary_key=True),
                         Column('fields_id',ForeignKey('fields.id'), primary_key=True))




# documents table
class Document(Base):
    #### This part is not change, is the same as above ####
    __tablename__='documents'

    # every column is an object of class Column
    # Integer, String: datatype
    # 'title', 'abstract': column label. optional
    id = Column(Integer, primary_key=True)

    title = Column('title', Text)

    abstract = Column('abstract', Text)

    publication_date = Column("publication_date", DateTime)

    submission_date = Column("submission_date", DateTime)

    online_date = Column('online_date', DateTime)

    revision_date = Column('revision_date', DateTime)

    accepted_date = Column('accepted_date', DateTime)



    coverpage_url = Column("cover_url", String(250))
    fulltext_url = Column("full_url", String(250))

    fpage = Column("first_page", Integer)
    lpage = Column("last_page", Integer)
    pages = Column("pages", Integer)

    document_type = Column("document_type", String(50))

    type = Column("type", String(30))

    articleid = Column("article_id",Integer)

    context_key = Column("context_key", Integer)

    label = Column("label", Integer)

    # publication_title=Column(String(100))

    submission_path = Column("submission_path", String(100))
    ##### So you can skip this part ####


    # this is corresponding to the register table above.
    # here we use the relationship() method

    authors = relationship("Author",
                         secondary=documents_authors,
                         back_populates="documents")

    keywords = relationship("Keyword",
                          secondary=documents_keywords,
                          back_populates="documents")

    fields = relationship('Field',
                        secondary=documents_fields,
                        back_populates="documents")

    #journal_id=Column(Integer, ForeignKey('journals.id'))
    #journal=relationship("Journal", back_populates="documents")
    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship("Source", back_populates="documents")


    def __repr__(self):
        return "<Document(title=%r)>" %self.title

# authors table
class Author(Base):
    __tablename__='authors'
    #### this part is in the same pattern of document table ####
    id= Column(Integer,primary_key=True)

    email=Column("email", String(80))
    institution=Column("institution", Text)

    lname=Column("last_name", String(80))
    fname=Column("first_name", String(80))
    mname=Column("middle_name", String(80))
    avatar = Column(String(250))
    address = Column(Text)
    vitae = Column(Text)


    ### these are mapping columns, the column labels are from the list: dbv_author. ###



    documents=relationship('Document',
                           secondary=documents_authors,
                           back_populates="authors")

    def __repr__(self):
        return "<Author(full_name=%r)>" %self.full_name



# keywords table
class Keyword(Base):
    __tablename__="keywords"
    id=Column(Integer, primary_key=True)

    keyword=Column(Text)

    documents=relationship("Document",
                           secondary=documents_keywords,
                           back_populates="keywords")

    def __repr__(self):
        return "<Keyword(keyword=%r)>" %self.keyword




# fields table
class Field(Base):
    __tablename__='fields'
    id=Column(Integer, primary_key=True)

    name=Column('name',String(100))
    type=Column('type',String(100))
    value=Column('value',Text)

    documents=relationship('Document',
                           secondary=documents_fields,
                           back_populates="fields")

    def __repr__(self):
        return "<Field(name=%r, type=%r, value=%r)>" %(self.name, self.type, self.value)


class Source(Base):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key = True)

    publication_title  = Column(String(100))
    chief_editor = Column(String(100))
    issn = Column(String(30))
    description = Column(Text)
    home_url = Column(String(250))
    coverimage = Column(String(250))


    documents = relationship("Document", back_populates = 'source')

    def __repr__(self):
        return "<Source(%s)>" %(self.publication_title)


'''

# This part can be concelled out, if you do not need.
class Journal(Base):
    __tablename__='journals'
    id=Column(Integer, primary_key=True)

    publication_title = Column('publication_title', String(200))
    domain=Column("domain",String(50))
    vol=Column("volume", String(50))
    iss=Column('issue', String(50))
    label=Column('label', String(50))

    documents=relationship("Document", back_populates="journal")

    def __repr__(self):
        return "<Journal(vol %r, iss %r)>" %(self.vol, self.iss)
'''
