import sys

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMessageBox, QWidget
from .databaseControl import DataBaseControl
from .tabHandler import TabHandler, Tab

# https://doc.qt.io/qtforpython/PySide6/QtWidgets/QLineEdit.html?highlight=qlineedit

StyleStr = """
            background-color: #4f3f5e;
            border-style: outset;
            border-width: 1px;
            border-radius: 5px;
            border-color: beige;
            font: bold 14px;
            color: white;
            min-width: 4em;
            padding: 6px;"""


class WebBrowser(QWidget):

    def __init__(self, *args, **kwargs):
        super(WebBrowser, self).__init__(*args, **kwargs)
        self.url_List = []
        self.database = DataBaseControl('sqlite:///webBrowser3.db')
        self.checkList = []
        self.check = False
        self.styleString = StyleStr
        self.startUrl = self.database.getStartUrl()

    def closeEvent(self, event):
        event.ignore()
        self.database.changeSize(self.width(), self.height(),
                                 self.isFullScreen())
        mBox = QMessageBox()
        result = mBox.question(self, "Confirm Exit",
                               "Are you sure you want to exit?",
                               QMessageBox.Yes | QMessageBox.No,
                               QMessageBox.No)
        if result == QMessageBox.Yes:
            event.accept()

    def mainWindow(self):

        self.setWindowTitle("Westerizz")
        self.resize(self.database.getSize().width,
                    self.database.getSize().height)
        self.setStyleSheet("color: white;  background-color: #4f3f5e")

        self.tabHandler = TabHandler(self)
        self.hBox = QHBoxLayout()

        self.setLayout(self.tabHandler)
        # self.setLayout(tab_widget)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    browser = WebBrowser()
    browser.mainWindow()
    sys.exit(app.exec_())
