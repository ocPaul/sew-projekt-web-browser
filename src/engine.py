from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class Engine(QWebEngineView):
    def __init__(self, database, urlBar, *args, **kwargs):
        super(Engine, self).__init__(*args, **kwargs)

        self.database = database
        self.urlBar = urlBar

    def navigate(self, url, tüt):
        self.checkList = ["http://", "https://", "https//"]
        self.check = False
        checkedUrl = self.database.getBookmarkTag(url)

        if checkedUrl != "":
            if self.urlBar.hasFocus() or tüt:
                for i in self.checkList:
                    if checkedUrl.startswith(i):
                        self.check = True
                if not self.check:
                    checkedUrl = "http://" + checkedUrl
                self.urlBar.setText(checkedUrl)
                self.setUrl(QUrl(checkedUrl))

    def goBack(self):
        self.back()

    def goForward(self):
        self.forward()

    def currentUrl(self):
        url = self.url().toString(QUrl.RemoveFragment)
        title = self.title()
        self.urlBar.setText(url)
        self.database.addHistory(url, title)
        return url
