from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import Qt
from databaseControl import *
import sys
import logging

class WebBrowser():

    def __init__(self, *args, **kwargs):
        super(WebBrowser, self).__init__(*args, **kwargs)
        self.url_List = []
        self.database = DataBaseControl()
        self.checkList = []
        self.check = False
        self.database.changeSize(1200, 200)
        
    def GUI(self):
        
        # self.app = QApplication([])
        self.mainWindow = QWidget()
        self.mainWindow.setWindowTitle("Westerizz")

        self.mainWindow.setMinimumSize(self.database.getSize().width, self.database.getSize().height)

        self.vBox = QVBoxLayout()
        self.hBox = QHBoxLayout()

        self.urlBar = QLineEdit()
        self.urlBar.setMaximumHeight(20)

        self.enterButton = QPushButton()
        self.enterButton.setIcon(QIcon('media/enter.png'))
        self.enterButton.setMinimumHeight(20)
        self.enterButton.clicked.connect(lambda: self.navigate(self.urlBar.text(), True))
        
        enterPressed = QShortcut(QKeySequence("Return"), self.urlBar)
        enterPressed.activated.connect(lambda: self.navigate(self.urlBar.text(), False))

        self.backButton = QPushButton("<")
        self.backButton.setMaximumSize(35,30)
        self.backButton.clicked.connect(lambda: self.goBack())
        # self.backButton.setStyleSheet("border :1px solid green")

        self.forwardButton = QPushButton(">")
        self.forwardButton.setMaximumSize(35,30)
        self.forwardButton.clicked.connect(lambda: self.goForward())

        self.hBox.addWidget(self.urlBar)
        self.hBox.addWidget(self.enterButton)
        self.hBox.addWidget(self.backButton)
        self.hBox.addWidget(self.forwardButton)

        startUrl = self.database.getStartUrl()
        self.engine = QWebEngineView()
        self.engine.setUrl(QUrl(startUrl))
        self.urlBar.setText(startUrl)
        self.engine.loadFinished.connect(self.currentUrl)

        self.vBox.addLayout(self.hBox)
        self.vBox.addWidget(self.engine)

        self.mainWindow.setLayout(self.vBox)
        self.mainWindow.show()

    def currentUrl(self):
        url = self.engine.url().toString(QUrl.RemoveFragment)
        title = self.engine.title()
        self.urlBar.setText(url)
        self.database.addHistory(url, title)

    def navigate(self, url, tüt):
        self.checkList = ["http://","https://", "https//"]
        self.check = False

        if url is not "":
            if self.urlBar.hasFocus() or tüt:
                for i in self.checkList:
                    if url.startswith(i):
                        self.check = True
                        
                if not self.check:
                    url = "http://" + url
                self.urlBar.setText(url)
                self.engine.setUrl(QUrl(url))

    def changeStartUrl():
        pass
    
    def goBack(self):
        self.engine.back()

    def goForward(self):
        self.engine.forward()


if __name__ == "__main__":
    app = QApplication([])
    browser = WebBrowser()
    browser.GUI()
    sys.exit(app.exec_())



        
