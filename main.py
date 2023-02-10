import sys
from src import WebBrowser
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    browser = WebBrowser()
    browser.mainWindow()
    sys.exit(app.exec_())
