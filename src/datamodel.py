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

    def __init__(self, url, title, visit_time, visit_count, duration):
        self.url = url
        self.title = title
        self.visit_time = visit_time
        self.visit_count = visit_count
        self.duration = duration
