from PyQt5.QtCore import QSize
from PyQt5.QtGui import QCursor, QIcon, QKeySequence
from PyQt5.QtWidgets import (QHBoxLayout, QLineEdit,
                             QMenu, QPushButton, QShortcut,
                             QVBoxLayout, QWidget)
from .engine import Engine
from .bookMarkGUI import ListBookmarkGUI, SaveBookmarkGUI
from .historyGUI import ListHistoryGUI
from .settingsGUI import SettingsGUI


class TabHandler(QVBoxLayout):

    def __init__(self, calledSelf, *args, **kwargs):
        super(TabHandler, self).__init__(*args, **kwargs)
        self.calledSelf = calledSelf
        self.tabBar = QHBoxLayout()
        self.tabHolder = QVBoxLayout()
        self.addTabButton = GPushButton("+", self.calledSelf.styleString)
        self.tabBar.addWidget(self.addTabButton)
        self.addLayout(self.tabBar)
        self.addLayout(self.tabHolder)
        self.addTab()
        self.addTabButton.clicked.connect(lambda: self.addTab())

    def addTab(self):
        self.tab = QWidgetTab(Tab(self.calledSelf))
        self.addTabButton.setVisible(False)
        # # self.tab.setup()
        # tabButton = TPushButton(self.tab, self, "Tab",
        #                         self.calledSelf.styleString)
        self.tabHolder.addWidget(self.tab)
        # self.tabBar.addWidget(tabButton)

    def switchTabs(self, tab):
        currentTab = self.tabHolder.takeAt(0)
        print(currentTab)
        print(tab)
        # if currentTab:
            # currentTab.setVisible(False)
        # self.tabHolder.insertLayout(0, tab)
        # tab.setVisible(True)


class QWidgetTab(QWidget):

    def __init__(self, tab, *args, **kwargs):
        super(QWidgetTab, self).__init__(*args, **kwargs)
        tab.setup()
        self.setLayout(tab)


class Tab(QVBoxLayout):

    def __init__(self, calledSelf, *args, **kwargs):
        super(Tab, self).__init__(*args, **kwargs)
        self.calledSelf = calledSelf

    def setup(self):
        self.hBox = QHBoxLayout()
        self.urlBar = UrlBarQLineEdit(self.calledSelf.styleString)
        self.urlBar.setMaximumHeight(40)
        self.enterButton = GPushButton("", self.calledSelf.styleString +
                                       "border: none;")
        # self.enterButton.style().setProperty("color", "red")
        self.enterButton.setIcon(QIcon('media/rocket1.png'))
        self.enterButton.setIconSize(QSize(50, 40))
        self.enterButton.setMinimumHeight(20)
        self.enterButton.clicked.connect(lambda: self.engine.navigate(
                                         self.urlBar.text(), True))

        enterPressed = QShortcut(QKeySequence("Return"), self.urlBar)
        enterPressed.activated.connect(lambda: self.engine.navigate(
                                       self.urlBar.text(), False))

        self.backButton = GPushButton("<", self.calledSelf.styleString)
        self.backButton.clicked.connect(lambda: self.engine.goBack())

        self.forwardButton = GPushButton(">", self.calledSelf.styleString)
        self.forwardButton.clicked.connect(lambda: self.engine.goForward())

        self.menuButton = GPushButton("menu", self.calledSelf.styleString)
        self.menuButton.clicked.connect(lambda: self.openMenu())

        self.hBox.addWidget(self.urlBar)
        self.hBox.addWidget(self.enterButton)
        self.hBox.addWidget(self.backButton)
        self.hBox.addWidget(self.forwardButton)
        self.hBox.addWidget(self.menuButton)

        self.engine = Engine(self.calledSelf.database, self.urlBar)
        self.engine.navigate(self.calledSelf.startUrl, True)

        self.urlBar.setText(self.calledSelf.startUrl)
        self.engine.loadFinished.connect(self.engine.currentUrl)

        self.addLayout(self.hBox)
        self.addWidget(self.engine)
        self.setContentsMargins(4, 4, 4, 4)

    def getTabUrl(self):
        return self.engine.currentUrl()

    def openMenu(self):
        menu = QMenu(self.calledSelf)
        menu.styleSheet()
        menu.addAction("Settings")
        menu.addSeparator()
        menu.addAction("Add Bookmark")
        menu.addAction("Bookmarks")
        menu.addSeparator()
        menu.addAction("History")
        menu.addSeparator()
        menu.addAction("Exit")
        action = menu.exec_(QCursor.pos())
        if action:
            if action.text() == "Exit":
                self.calledSelf.close()
            if action.text() == "Settings":
                self.settings = SettingsGUI(self.calledSelf.database,
                                            self.calledSelf.styleString)
                self.settings.show()
            if action.text() == "Add Bookmark":
                self.addBookmark = SaveBookmarkGUI(self.calledSelf.database,
                                                   self.engine,
                                                   self.calledSelf.styleString)
                self.addBookmark.show()
            if action.text() == "Bookmarks":
                self.bookmarks = ListBookmarkGUI(self.calledSelf.database,
                                                 self.engine,
                                                 self.calledSelf.styleString)
                self.bookmarks.show()
            if action.text() == "History":
                self.history = ListHistoryGUI(self.calledSelf.database,
                                                 self.engine,
                                                 self.calledSelf.styleString)
                self.history.show()


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


class TPushButton(GPushButton):
    def __init__(self, tab, seelfe, *args, **kwargs):
        super(TPushButton, self).__init__(*args, **kwargs)
        self.tab = tab
        self.seelfe = seelfe
        # self.seelfe.switchTabs(self.tab)
        super().clicked.connect(self.switchTabs)

    def switchTabs1(self):
        print(self.tab.getTabUrl())
        currentTab = self.tabHolder.takeAt(0)
        self.tabHolder.removeItem(currentTab)
        self.tabHolder.insertLayout(0, self.tab)

    def switchTabs(self):
        print("tswitchTabs")
        self.seelfe.switchTabs(self.tab)


class UrlBarQLineEdit(QLineEdit):

    def __init__(self, styleString, *args, **kwargs):
        super(UrlBarQLineEdit, self).__init__(*args, **kwargs)
        self.styleString = styleString
        self.setStyleSheet(self.styleString)
        self.focus = False

    def focusInEvent(self, event):
        self.focus = True
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
        if self.focus is False:
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
        if self.focus is False:
            self.setStyleSheet(self.styleString)
