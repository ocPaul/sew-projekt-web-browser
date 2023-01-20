from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datamodel import Base, Bookmark, Config, History
from sqlalchemy.sql import func

class DataBaseControl:
    
    def __init__(self):
        self.engine = create_engine('sqlite:///webBrowser.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def addBookmark(self, url, title, description):
        data = Bookmark(url=url, title=title, description=description)
        self.session.add(data)
        self.session.commit()

    def addHistory(self, url, title):
        data = History(url=url, title=title, dateTime=func.now())
        self.session.add(data)
        self.session.commit()

    def changeStartUrl(self, startUrl):
        if not startUrl.startswith("http://"):
                startUrl = "http://" + startUrl
            
        self.session.query(Config).filter(Config.id == 1).update({Config.startUrl: startUrl})
        self.session.commit()

    def changeSize(self, width, height):
        self.session.query(Config).filter(Config.id == 1).update({Config.width: width, Config.height: height})
        self.session.commit()

    def getBookmarks(self):
        return self.session.query(Bookmark).all()

    def getStartUrl(self):
        return self.session.query(Config).filter(Config.id == 1).first().startUrl

    def getSize(self):
                
        return self.session.query(Config).filter(Config.id == 1).first()
 