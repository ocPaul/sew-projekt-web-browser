from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from databaseControl import *
import sys


class WebBrowser(QWidget):

    def __init__(self, *args, **kwargs):
        super(WebBrowser, self).__init__(*args, **kwargs)
        self.url_List = []
        self.database = DataBaseControl()
        self.checkList = []
        self.check = False
        # self.settings = settingsGUI(self.database)

    def closeEvent(self, event):
        event.ignore()
        self.database.changeSize(self.width(), self.height())
        mBox = QMessageBox()
        result = mBox.question(self, "Confirm Exit", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            event.accept()

    def mainWindow(self):

        # self.mainWindow = QWidget()
        self.setWindowTitle("Westerizz")
        self.resize(self.database.getSize().width, self.database.getSize().height)
        # print(self.width())

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

        self.menuButton = QPushButton("menu")
        self.menuButton.clicked.connect(lambda: self.openMenu())

        self.hBox.addWidget(self.urlBar)
        self.hBox.addWidget(self.enterButton)
        self.hBox.addWidget(self.backButton)
        self.hBox.addWidget(self.forwardButton)
        self.hBox.addWidget(self.menuButton)

        startUrl = self.database.getStartUrl()
        self.engine = QWebEngineView()
        self.engine.setUrl(QUrl(startUrl))
        self.urlBar.setText(startUrl)
        self.engine.loadFinished.connect(self.currentUrl)

        self.vBox.addLayout(self.hBox)
        self.vBox.addWidget(self.engine)

        self.setLayout(self.vBox)
        self.show()

    def currentUrl(self):
        url = self.engine.url().toString(QUrl.RemoveFragment)
        title = self.engine.title()
        self.urlBar.setText(url)
        self.database.addHistory(url, title)

    def navigate(self, url, tüt):
        self.checkList = ["http://", "https://", "https//"]
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

    def openMenu(self):
        menu = QMenu(self)
        menu.addAction("Settings")
        menu.addAction("Add Bookmark")
        menu.addSeparator()
        menu.addAction("Exit")
        action = menu.exec_(QCursor.pos())
        if action:
            if action.text() == "Exit":
                self.close()
            if action.text() == "Settings":
                self.settings = settingsGUI(self.database)
                self.settings.show()
            if action.text() == "Add Bookmark":
                self.bookmarks = bookmarkGUI(self.database, self.engine)
                self.bookmarks.show()

class settingsGUI(QWidget):
        
        def __init__(self, database):
            super().__init__()

            self.database = database
            vBox = QVBoxLayout()
            hBox1= QHBoxLayout()

            self.title = QLabel("Settings:")            
            self.startUrlLine = QLineEdit(self.database.getStartUrl())
            self.urlLabel = QLabel("Start Url:")
            
            hBox1.addWidget(self.urlLabel)            
            hBox1.addWidget(self.startUrlLine)

            vBox.addWidget(self.title)
            vBox.addLayout(hBox1)

            self.setLayout(vBox)
            # self.setFixedSize()
        
        def closeEvent(self, event):
            self.database.changeStartUrl(self.startUrlLine.text())

class bookmarkGUI(QWidget):
        
        def __init__(self, database, engine):
            super().__init__()

            self.engine = engine
            self.database = database

            vBox = QVBoxLayout()
            hBox1 = QHBoxLayout()
            hBox2 = QHBoxLayout()
            hBox3 = QHBoxLayout()
            hBox4 = QHBoxLayout()

            self.title = QLabel("Add Bookmark:")

            self.url = QLineEdit(self.engine.url().toString(QUrl.RemoveFragment))
            self.urlLabel = QLabel("Url:")
            
            self.pageTitle = QLineEdit(self.engine.title())
            self.pageTitleLabel = QLabel("Title:")
            
            self.desc = QLineEdit("")
            self.descLabel = QLabel("Description:")

            self.tags = QLineEdit("")
            self.tagsLabel = QLabel("tags:")
            
            self.saveButton = QPushButton("save")
            self.saveButton.clicked.connect(lambda: self.saveData())
            
            hBox1.addWidget(self.urlLabel)            
            hBox1.addWidget(self.url)

            hBox2.addWidget(self.pageTitleLabel)
            hBox2.addWidget(self.pageTitle)

            hBox3.addWidget(self.descLabel)
            hBox3.addWidget(self.desc)

            hBox4.addWidget(self.tagsLabel)
            hBox4.addWidget(self.tags)

            vBox.addWidget(self.title)
            vBox.addLayout(hBox1)
            vBox.addLayout(hBox2)
            vBox.addLayout(hBox3)
            vBox.addLayout(hBox4)
            vBox.addWidget(self.saveButton)

            self.setLayout(vBox)

        def saveData(self):
            self.database.addBookmark(self.url.text(), self.pageTitle.text(), self.desc.text(), self.tags.text())
            self.close()
        
        # def closeEvent(self, event):
        #     self.database.changeStartUrl(self.url.text())


if __name__ == "__main__":
    app = QApplication([])
    browser = WebBrowser()
    browser.mainWindow()
    sys.exit(app.exec_())    
