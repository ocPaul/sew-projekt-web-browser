import pytest

from src import DataBaseControl
from sqlalchemy.sql import func

def test_inital_():
    assert 1 == 1


def test_addBookmark():
    database = DataBaseControl('sqlite:///:memory:')
    database.addBookmark("juhui.com", "JUHUI", ":D", "guten Tag")
    bookmarks = database.getBookmarks()
    assert bookmarks[0].url == "juhui.com"
    assert bookmarks[0].title == "JUHUI"
    assert bookmarks[0].description == ":D"
    assert bookmarks[0].tag == "guten Tag"


def test_addHistory():
    database = DataBaseControl('sqlite:///:memory:')
    database.addHistory("juhui.com", "JUHUI")
    time = str(func.now())
    history = database.getHistory()

    assert history[0].url == "juhui.com"
    assert history[0].title == "JUHUI"
    # assert str(history[0].dateTime) == time gaxe :D /:


def test_changeStartUrl():
    database = DataBaseControl('sqlite:///:memory:')
    database.changeStartUrl("afad.com")

    assert database.getStartUrl() == "http://afad.com"


def test_change_Size():
    database = DataBaseControl('sqlite:///:memory:')
    database.changeSize(25, 52, False)
    size = database.getSize()

    assert size.width == 25
    assert size.height == 52
    assert size.fullscreen is False
