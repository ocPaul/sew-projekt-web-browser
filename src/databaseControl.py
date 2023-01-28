from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists, func, text

from datamodel import Base, Bookmark, Config, History


class DataBaseControl:

    def __init__(self):
        self.engine = create_engine('sqlite:///webBrowser3.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.__checkConfigEntry()

    def addBookmark(self, url, title, description, tag):
        data = Bookmark(url=url, title=title, description=description, tag=tag)
        self.session.add(data)
        self.session.commit()

    def dellBookmark(self, id):
        self.session.query(Bookmark).filter(Bookmark.id == id).delete(
                    synchronize_session='fetch')
        self.session.commit()

    def addHistory(self, url, title):
        data = History(url=url, title=title, dateTime=func.now())
        self.session.add(data)
        self.session.commit()

    def changeStartUrl(self, startUrl):
        if not startUrl.startswith("http://"):
            startUrl = "http://" + startUrl

        self.session.query(Config).filter(Config.id == 1).update(
                    {Config.startUrl: startUrl})
        self.session.commit()

    def changeSize(self, width, height, fullscreen):
        self.session.query(Config).filter(Config.id == 1).update(
                    {Config.width: width, Config.height: height,
                     Config.fullscreen: fullscreen})
        self.session.commit()

    def getBookmarks(self):
        bookmarks = self.session.query(Bookmark).all()
        return bookmarks

    def getBookmarkTag(self, input):
        if self.session.query(exists().where(Bookmark.tag == input)).scalar():
            return self.session.query(Bookmark).filter(
                    Bookmark.tag == input).first().url
        else:
            return input

    def getStartUrl(self):
        return self.session.query(Config).filter(
                    Config.id == 1).first().startUrl

    def getSize(self):
        self.__checkConfigEntry()
        return self.session.query(Config).filter(Config.id == 1).first()

    def __checkConfigEntry(self):
        if (self.session.execute(text('SELECT COUNT(*) FROM config')
                                 ).scalar() < 1):
            data = Config(startUrl="google.at",
                          width=700, heigth=500,
                          fullscreen=False)
            self.session.add(data)
            self.session.commit()


if __name__ == "__main__":
    database = DataBaseControl()
