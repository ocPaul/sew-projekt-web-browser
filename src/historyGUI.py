from PyQt5 import Qt
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import (QHBoxLayout, QLineEdit,
                             QVBoxLayout, QWidget)


class ListHistoryGUI(QWidget):
    def __init__(self, database, engine, styleString, *args, **kwargs):
        super(ListHistoryGUI, self).__init__(*args, **kwargs)
        self.styleString = styleString
        self.setStyleSheet(styleString)

        self.engine = engine
        self.history = database.getHistory()

        self.setWindowTitle("History")

        vBox = QVBoxLayout()

        for i in range(len(self.history)):
            urlLine = historyGUIButtons(self.history[i].url, self.engine,
                                        self.history[i].url,
                                        self.styleString)
            titleLine = historyGUIButtons(self.history[i].title,
                                          self.engine,
                                          self.history[i].url,
                                          self.styleString)
            timeLine = historyGUIButtons(str(self.history[i].dateTime), self.engine,
                                         self.history[i].url,
                                         self.styleString)

            hBox = QHBoxLayout()
            hBox.addWidget(urlLine)
            hBox.addWidget(titleLine)
            hBox.addWidget(timeLine)

            vBox.addLayout(hBox)
        vBox.setSpacing(0)
        self.setLayout(vBox)


class historyGUIButtons(QLineEdit):

    def __init__(self, input, engine, url, styleString, *args, **kwargs):
        super(historyGUIButtons, self).__init__(*args, **kwargs)
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
