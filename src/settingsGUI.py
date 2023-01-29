import sys

from PyQt5 import Qt
from PyQt5.QtCore import QEvent, QSize, QUrl, Qt
from PyQt5.QtGui import QCursor, QIcon, QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QMenu, QMessageBox, QPushButton, QShortcut,
                             QVBoxLayout, QWidget)


class SettingsGUI(QWidget):

    def __init__(self, database, styleString):
        super().__init__()

        self.database = database
        self.styleString = styleString

        self.setWindowTitle("Settings")
        self.resize(300, 50)
        self.setStyleSheet(self.styleString)

        vBox = QVBoxLayout()
        hBox = QHBoxLayout()

        self.title = QLabel("Settings:")
        self.startUrlLine = QLineEdit(self.database.getStartUrl())
        self.urlLabel = QLabel("Start Url:")

        hBox.addWidget(self.urlLabel)
        hBox.addWidget(self.startUrlLine)

        vBox.addWidget(self.title)
        vBox.addLayout(hBox)

        self.setLayout(vBox)