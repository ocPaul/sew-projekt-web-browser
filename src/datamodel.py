from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Bookmark(Base):
    __tablename__ = 'bookmarks'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    description = Column(String)
    tag = Column(String)

    def __init__(self, url, title, description, tag):
        self.url = url
        self.title = title
        self.description = description
        self.tag = tag


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


class Style(Base):
    __tablename__ = 'Style'

    id = Column(Integer, primary_key=True)
    widget = Column(String)
    mainColor = Column(String)
    secondColor = Column(String)
    border = Column(Boolean)
    borderRadius = Column(Integer)
    font = Column(String)


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    startUrl = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    fullscreen = Column(Boolean)

    def __init__(self, startUrl, width, heigth, fullscreen):
        self.startUrl = startUrl
        self.width = width
        self.height = heigth
        self.fullscreen = fullscreen
