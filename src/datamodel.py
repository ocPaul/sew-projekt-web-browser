from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bookmark(Base):
    __tablename__ = 'bookmarks'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    description = Column(String)

    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    dateTime = Column(DateTime)

    def __init__(self, url, title, dateTime):
        self.url = url
        self.title = title
        self.dateTime = dateTime


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    startUrl = Column(String)
    width = Column(Integer)
    height = Column(Integer)     

    def __init__(self, startUrl, width, heigth):
        self.startUrl = startUrl
        self.width = width
        self.height = heigth
           
