#!/bin/python3
import sys, os, json, urllib, platform
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import PyQt5.QtWebEngineWidgets as webengwid

_sf = open("settings.json")
settings = json.loads(_sf.read())
_sf.close()


iconext = "png"
iswin = platform.win32_ver()[0] != ""
ismac = platform.mac_ver()[0] != ""
isunix = platform.libc_ver()[0] != ""

if iswin: iconext = "ico"
if ismac: iconext = "icns"


HOMEPAGE_URL = settings.get("homepage")


BROWSER_SE = settings.get("search_engine").get(settings.get("search_engine").get("current"))


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        rect = app.primaryScreen().geometry()
        self.title = "UCI Browser"
        self.width = settings.get("startup").get("size")[0]
        self.height = settings.get("startup").get("size")[1]
        self.top = rect.height() / 2 - self.height / 2
        self.left = rect.width() / 2 - self.width / 2
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon(f"./icon/i.{iconext}"))

        if settings.get("startup").get("maximized") == True:
            self.showMaximized()




        self.browser = webengwid.QWebEngineView()

        

        self.navbar = QToolBar()

        browser_goback = QAction("<", self)
        browser_goback.triggered.connect(self.browser.back)
        self.navbar.addAction(browser_goback)

        browser_gofwd = QAction(">", self)
        browser_gofwd.triggered.connect(self.browser.forward)
        self.navbar.addAction(browser_gofwd)

        browser_reload = QAction("R", self)
        browser_reload.triggered.connect(self.browser.reload)
        self.navbar.addAction(browser_reload)

        browser_gohome = QAction("H", self)
        browser_gohome.triggered.connect(lambda: self.go_to_url(HOMEPAGE_URL))
        self.navbar.addAction(browser_gohome)

        self.browser_urlbar = QLineEdit()
        self.browser_urlbar.returnPressed.connect(lambda: self.go_to_url(None))
        self.navbar.addWidget(self.browser_urlbar)

        self.browser.urlChanged.connect(lambda: self.set_urlbar_url(None))
        self.browser.titleChanged.connect(lambda: self.setWindowTitle(self.browser.title() + " - UCI Browser"))





        self.pagebar = QToolBar() 

        newpagetab = QAction("+", self) 
        newpagetab.triggered.connect(lambda: self.new_page(HOMEPAGE_URL))
        self.pagebar.addAction(newpagetab)



        self.addToolBar(self.pagebar)
        self.addToolBar(self.navbar)
        self.setCentralWidget(self.browser)
        self.show()


        self.new_page(HOMEPAGE_URL)





    def go_to_url(self, url):
        urltg = url
        if url == None:
            urltg = self.browser_urlbar.text()

        if urltg.find(".") > 0 and urltg.find("/") > 0:
            if not urltg.startswith("https://" or "http://"):
                urltg = "https://" + urltg
        else:
            urltg = BROWSER_SE + urllib.parse.quote(urltg)

        print(urltg)

        self.browser.setUrl(QUrl(urltg))

    def set_urlbar_url(self, url):
        urll = url
        if url == None:
            _url = self.browser.url().toString()
            self.browser_urlbar.setText(_url)
            urll = _url
        else:
            self.browser_urlbar.setText(url) 

        history = ""

        if os.path.exists(f"{os.getcwd()}/history") == False:
            _f = open("history", "w+")
            _f.write("")
            _f.close()
        else:
            _f = open("history", "r+")
            history = _f.read() 
            _f.close()

        _hf = open("history", "w+")

        history += "\n" + urll 

        _hf.write(history) 
        _hf.close()





    def new_page(self, url):
        page = webengwid.QWebEnginePage() 
        if url == None:
            url = HOMEPAGE_URL
        else: url = QUrl(url) 

        page.setUrl(url)

        self.browser.setPage(page)

        
        acitem = QAction(url.toString()) 
        acitem.triggered.connect(lambda: self.browser.setPage(page))
        page.titleChanged.connect(lambda: self.set_page_title(page, acitem))

        closebtn = QAction("-X|")
        closebtn.triggered.connect(lambda: self.close_page(acitem, closebtn)) 

        self.pagebar.addAction(acitem)
        self.pagebar.addAction(closebtn)

    def set_page_title(self, page, acitem):
        title = page.title()
        _title = title

        maxlen = settings.get("misc").get("max_page_title_length")

        if len(title) > maxlen:
            title = ""
            for i in range(maxlen):
                title += _title[i]

        acitem.setText(title)

    def close_page(self, acitem, closebtn):
        self.pagebar.removeAction(acitem)
        self.pagebar.removeAction(closebtn)

        

if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    ex = App()
    app.exec_()
