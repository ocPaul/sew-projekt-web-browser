from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import Qt
import sys

class WebBrowser():

    def __init__(self, *args, **kwargs):
        super(WebBrowser, self).__init__(*args, **kwargs)
        self.url_List = []

    def GUI(self, starturl="http://google.com"):
        
        # self.app = QApplication([])
        self.mainWindow = QWidget()
        self.mainWindow.setWindowTitle("Westerizz")

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

        self.engine = QWebEngineView()
        self.engine.setUrl(QUrl(starturl))
        self.current_url = self.engine.url()
        self.engine.urlChanged.connect(self.urlSave)

        self.vBox.addLayout(self.hBox)
        self.vBox.addWidget(self.engine)

        self.mainWindow.setLayout(self.vBox)
        self.mainWindow.show()

    def urlSave(self):
        url = self.engine.url().toString(QUrl.RemoveFragment)
        # url = self.engine.url()
        print(url)
        self.url_List.append(url)
    
    def navigate(self, url, tüt):
        if self.urlBar.hasFocus() or tüt:
            if not url.startswith("http://"):
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



        
