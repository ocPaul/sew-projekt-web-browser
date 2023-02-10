from PyQt5 import Qt
from PyQt5.QtCore import QEvent, QSize, QUrl, Qt
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QLineEdit,
                             QPushButton,
                             QVBoxLayout, QWidget)


class SaveBookmarkGUI(QWidget):

    def __init__(self, database, engine, styleString):
        super().__init__()

        self.engine = engine
        self.database = database
        self.styleString = styleString

        self.setWindowTitle("Add Bookmark")
        self.setStyleSheet(self.styleString)
        self.setFixedSize(QSize(315, 259))
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

        vBox.setAlignment(Qt.AlignTop)
        self.setLayout(vBox)

    def saveData(self):
        self.database.addBookmark(self.url.text(), self.pageTitle.text(),
                                  self.desc.text(), self.tag.text())
        self.close()

    def closeEvent(self, event):
        print(self.size())


class ListBookmarkGUI(QWidget):
    def __init__(self, database, engine, styleString, *args, **kwargs):
        super(ListBookmarkGUI, self).__init__(*args, **kwargs)
        self.styleString = styleString
        self.setStyleSheet(styleString)

        self.engine = engine
        self.bookmarks = database.getBookmarks()

        self.setWindowTitle("Bookmarks")

        vBox = QVBoxLayout()

        for i in range(len(self.bookmarks)):
            urlLine = BookMarkGuiButtons(self.bookmarks[i].url, self.engine,
                                         self.bookmarks[i].url,
                                         self.styleString)
            titleLine = BookMarkGuiButtons(self.bookmarks[i].title,
                                           self.engine,
                                           self.bookmarks[i].url,
                                           self.styleString)
            descriptionLine = BookMarkGuiButtons(self.bookmarks[i].description,
                                                 self.engine,
                                                 self.bookmarks[i].url,
                                                 self.styleString)
            tagLine = BookMarkGuiButtons(self.bookmarks[i].tag, self.engine,
                                         self.bookmarks[i].url,
                                         self.styleString)

            hBox = QHBoxLayout()
            hBox.addWidget(urlLine)
            hBox.addWidget(titleLine)
            hBox.addWidget(descriptionLine)
            hBox.addWidget(tagLine)

            vBox.addLayout(hBox)
        vBox.setSpacing(0)
        self.setLayout(vBox)


class BookMarkGuiButtons(QLineEdit):

    def __init__(self, input, engine, url, styleString, *args, **kwargs):
        super(BookMarkGuiButtons, self).__init__(*args, **kwargs)
        self.url = url
        self.input = input
        self.engine = engine
        self.setText(self.input)
        self.setReadOnly(True)
        self.first = False
        self.styleString = styleString
        self.setStyleSheet(self.styleString)

    def focusInEvent(self, event):
        event.ignore
        if self.first:
            self.engine.navigate(self.url, True)
        self.first = True

    def mousePressEvent(self, event):
        if (event.type() == QEvent.MouseButtonDblClick
           and event.button() == Qt.LeftButton):  
            self.selectAll()
            self.setReadOnly(False)
        super().mousePressEvent(event)
