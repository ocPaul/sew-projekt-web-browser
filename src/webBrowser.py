from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from databaseControl import *
import sys

"""https://doc.qt.io/qtforpython/PySide6/QtWidgets/QLineEdit.html?highlight=qlineedit"""

StyleStr = """
            background-color: #4f3f5e;
            border-style: outset;
            border-width: 1px;
            border-radius: 5px;
            border-color: beige;
            font: bold 14px;
            min-width: 4em;
            padding: 6px;"""


class WebBrowser(QWidget):

    def __init__(self, *args, **kwargs):
        super(WebBrowser, self).__init__(*args, **kwargs)
        self.url_List = []
        self.database = DataBaseControl()
        self.checkList = []
        self.check = False
        self.styleString = StyleStr
        self.startUrl = self.database.getStartUrl()

    def closeEvent(self, event):
        event.ignore()
        self.database.changeSize(self.width(), self.height())
        mBox = QMessageBox()
        result = mBox.question(self, "Confirm Exit", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            event.accept()

    def mainWindow(self):

        self.setWindowTitle("Westerizz")
        self.resize(self.database.getSize().width, self.database.getSize().height)
        self.setStyleSheet("color: white;  background-color: #4f3f5e")

        self.vBox = QVBoxLayout()
        self.hBox = QHBoxLayout()

        self.urlBar = UrlBarQLineEdit(self.styleString)
        self.urlBar.setMaximumHeight(40)

        self.enterButton = GPushButton("", self.styleString + "border: none;")
        # self.enterButton.style().setProperty("color", "red")
        self.enterButton.setIcon(QIcon('media/rocket1.png'))
        self.enterButton.setIconSize(QSize(50,40))
        self.enterButton.setMinimumHeight(20)
        self.enterButton.clicked.connect(lambda: self.engine.navigate(self.urlBar.text(), True))
        
        enterPressed = QShortcut(QKeySequence("Return"), self.urlBar)
        enterPressed.activated.connect(lambda: self.engine.navigate(self.urlBar.text(), False))

        self.backButton = GPushButton("<", self.styleString)
        self.backButton.clicked.connect(lambda: self.goBack())

        self.forwardButton = GPushButton(">", self.styleString)
        self.forwardButton.clicked.connect(lambda: self.engine.goForward())

        self.menuButton = GPushButton("menu", self.styleString)
        self.menuButton.clicked.connect(lambda: self.openMenu())

        self.hBox.addWidget(self.urlBar)
        self.hBox.addWidget(self.enterButton)
        self.hBox.addWidget(self.backButton)
        self.hBox.addWidget(self.forwardButton)
        self.hBox.addWidget(self.menuButton)


        self.engine = engine(self.database, self.urlBar)
        self.engine.navigate(self.startUrl, True)
        self.urlBar.setText(self.startUrl)
        self.engine.loadFinished.connect(self.engine.currentUrl)

        self.vBox.addLayout(self.hBox)
        self.vBox.addWidget(self.engine)

        self.setLayout(self.vBox)
        self.show()

    def currentUrl(self):
        url = self.engine.url().toString(QUrl.RemoveFragment)
        title = self.engine.title()
        self.urlBar.setText(url)
        self.database.addHistory(url, title)

    def goBack(self):
        self.engine.back()

    def goForward(self):
        self.engine.forward()

    def openMenu(self):
        menu = QMenu(self)
        menu.styleSheet()
        menu.addAction("Settings")
        menu.addAction("Add Bookmark")
        menu.addAction("Bookmarks")
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
                self.addBookmark = saveBookmarkGUI(self.database, self.engine)
                self.addBookmark.show()
            if action.text() == "Bookmarks":
                self.bookmarks = listBookmarkGUI(self.database, self.engine)
                self.bookmarks.show()

class engine(QWebEngineView):
    def __init__(self, database, urlBar, *args, **kwargs):
        super(engine, self).__init__(*args, **kwargs)

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

class GPushButton(QPushButton):
    
    def __init__(self, text, styleString, *args, **kwargs):
        super(GPushButton, self).__init__(*args, **kwargs)
        self.styleString = styleString
        self.setStyleSheet(self.styleString)
        self.setFixedHeight(40)
        self.setText(text)

    def enterEvent(self, event):
        self.setStyleSheet(
            """ background-color: #655178;
            border-style: outset;
            border-width: 1px;
            border-radius: 5px;
            border-color: beige;
            font: bold 14px;
            min-width: 4em;
            padding: 6px;""")
        
    def leaveEvent(self, event):
        self.setStyleSheet(self.styleString)

class UrlBarQLineEdit(QLineEdit):
    
    def __init__(self, styleString,*args, **kwargs):
        super(UrlBarQLineEdit, self).__init__(*args, **kwargs)
        self.styleString = styleString
        self.setStyleSheet(self.styleString)
        self.focus = False

    def focusInEvent(self, event):
        self.focus = True
        self.selectAll()
        self.setStyleSheet(
            """ background-color: #9685a8;
            border-style: outset;
            border-width: 1px;
            border-radius: 5px;
            border-color: beige;
            font: bold 14px;
            min-width: 4em;
            padding: 6px;""")

    def focusOutEvent(self, event):
        self.deselect()
        self.focus = False
        self.setStyleSheet(self.styleString)

    def enterEvent(self, event):
        if self.focus == False:
            self.setStyleSheet(
                """ background-color: #6e627a;
                border-style: outset;
                border-width: 1px;
                border-radius: 5px;
                border-color: beige;
                font: bold 14px;
                min-width: 4em;
                padding: 6px;""")
        
    def leaveEvent(self, event):
        if self.focus == False:
            self.setStyleSheet(self.styleString)

class settingsGUI(QWidget):
        
        def __init__(self, database):
            super().__init__()

            self.database = database

            self.setWindowTitle("Settings")
            self.resize(300, 50)

            vBox = QVBoxLayout()
            hBox= QHBoxLayout()

            self.title = QLabel("Settings:")            
            self.startUrlLine = QLineEdit(self.database.getStartUrl())
            self.urlLabel = QLabel("Start Url:")
            
            hBox.addWidget(self.urlLabel)            
            hBox.addWidget(self.startUrlLine)

            vBox.addWidget(self.title)
            vBox.addLayout(hBox)

            self.setLayout(vBox)
        
        def closeEvent(self, event):
            self.database.changeStartUrl(self.startUrlLine.text())

class saveBookmarkGUI(QWidget):
        
        def __init__(self, database, engine):

            super().__init__()

            self.engine = engine
            self.database = database

            self.setWindowTitle("Add Bookmark")
            # self.setWindowIcon("C:\Users\pauls\Documents\repos\sew-projekt-web-browser-1\media\bookmarkIco.png")

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

            self.tag = QLineEdit("")
            self.tagsLabel = QLabel("tag:")
            
            self.saveButton = QPushButton("save")
            self.saveButton.clicked.connect(lambda: self.saveData())
            
            hBox1.addWidget(self.urlLabel)            
            hBox1.addWidget(self.url)

            hBox2.addWidget(self.pageTitleLabel)
            hBox2.addWidget(self.pageTitle)

            hBox3.addWidget(self.descLabel)
            hBox3.addWidget(self.desc)

            hBox4.addWidget(self.tagsLabel)
            hBox4.addWidget(self.tag)

            vBox.addWidget(self.title)
            vBox.addLayout(hBox1)
            vBox.addLayout(hBox2)
            vBox.addLayout(hBox3)
            vBox.addLayout(hBox4)
            vBox.addWidget(self.saveButton)

            self.setLayout(vBox)

        def saveData(self):
            self.database.addBookmark(self.url.text(), self.pageTitle.text(), self.desc.text(), self.tag.text())
            self.close()

class listBookmarkGUI(QWidget):
    def __init__(self, database, engine,*args, **kwargs):
        super(listBookmarkGUI, self).__init__(*args, **kwargs)
        
        self.engine = engine
        self.database = database
        self.bookmarks = database.getBookmarks()

        self.setWindowTitle("Bookmarks")

        vBox = QVBoxLayout()

        for i in range(len(self.bookmarks)):
            urlLine = bookMarkGuiButtons(self.bookmarks[i].url, self.engine, self.bookmarks[i].url)
            titleLine = bookMarkGuiButtons(self.bookmarks[i].title, self.engine, self.bookmarks[i].url)
            descriptionLine = bookMarkGuiButtons(self.bookmarks[i].description, self.engine, self.bookmarks[i].url)
            tagLine = bookMarkGuiButtons(self.bookmarks[i].tag, self.engine, self.bookmarks[i].url)

            hBox= QHBoxLayout()
            hBox.addWidget(urlLine)
            hBox.addWidget(titleLine)
            hBox.addWidget(descriptionLine)
            hBox.addWidget(tagLine)

            vBox.addLayout(hBox)

        self.setLayout(vBox)

class bookMarkGuiButtons(QLineEdit):
    
    def __init__(self, input, engine, url, *args, **kwargs):
        super(bookMarkGuiButtons, self).__init__(*args, **kwargs)
        self.url = url
        self.input = input
        self.engine = engine
        self.setText(self.input)
        self.setReadOnly(True)

    def focusInEvent(self, event):
        event.ignore
        self.engine.navigate(self.url, True)

    def mousePressEvent(self, event):
        if event.type() == QEvent.MouseButtonDblClick and event.button() == Qt.LeftButton:
            print("blibla")
            self.selectAll()
            self.setReadOnly(False)
        super().mousePressEvent(event)

    


if __name__ == "__main__":
    app = QApplication([])
    browser = WebBrowser()
    browser.mainWindow()
    sys.exit(app.exec_())    
