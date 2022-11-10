#!/bin/python3

# libs, libs, libs
import sys, os, json, urllib, platform, threading, requests
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import PyQt5.QtWebEngineWidgets as webengwid
from PyQt5.QtWebEngineWidgets import QWebEngineView as webview

# modules
sys.path.append(os.path.relpath("modules"))

import tld_check, pages, settings_

settings = settings_.check()


# check for icon
iconext = "png"
iswin = platform.win32_ver()[0] != ""
ismac = platform.mac_ver()[0] != ""
isunix = platform.libc_ver()[0] != ""

if iswin: iconext = "ico"
if ismac: iconext = "icns"


# get homepage from settings
HOMEPAGE_URL = settings.get("homepage")

# and here search engine
SEARCH_ENGINE = settings.get("search_engine")
CURR_SE = SEARCH_ENGINE.get("current")
BROWSER_SE = SEARCH_ENGINE.get(CURR_SE)

# check for all TLDs in cloud
tld_check.check_for_tlds()




# and the actual app
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.BROWSER_SE = BROWSER_SE


        STARTUP_SIZE = settings.get("startup").get("size")
        rect = app.primaryScreen().geometry()
        self.title = "UCI Browser"
        self.width = int(STARTUP_SIZE[0])
        self.height = int(STARTUP_SIZE[1])
        self.top = int(rect.height() / 2 - self.height / 2)
        self.left = int(rect.width() / 2 - self.width / 2)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon(f"./icon/i.{iconext}"))
        self.mwid = QWidget(self) 
        self.grlt = QGridLayout() 
        self.mwid.setStyleSheet("background: #11111b;") 
        self.mwid.setLayout(self.grlt)

        self.grlt.setContentsMargins(QMargins(0, 0, 0, 0))

        # if it's set to maximized in settings 
        # then do so
        if settings.get("startup").get("maximized") == True:
            self.showMaximized()


        # main view 
        self.browser = webview()
        self.grlt.addWidget(self.browser, 0, 0, 0, 0)
        self.prev_page = self.browser

        # navbar no. 1
        self.navbar = QToolBar()

        # navbar buttons
        browser_goback = QAction("<", self)
        browser_goback.triggered.connect(self.browser.back)
        self.navbar.addAction(browser_goback)

        browser_gofwd = QAction(">", self)
        browser_gofwd.triggered.connect(self.browser.forward)
        self.navbar.addAction(browser_gofwd)

        browser_reload = QAction("↻", self)
        browser_reload.triggered.connect(self.browser.reload)
        self.navbar.addAction(browser_reload)

        browser_gohome = QAction("🏠", self)
        browser_gohome.triggered.connect(lambda: pages.go_to_url(self, HOMEPAGE_URL))
        self.navbar.addAction(browser_gohome)

        self.browser_urlbar = QLineEdit()
        self.browser_urlbar.returnPressed.connect(lambda: pages.go_to_url(self, None))
        self.navbar.addWidget(self.browser_urlbar)




        # navbar no.2
        # actually pagebar, for tabs
        self.pagebar = QToolBar()
        self.pagebar.move(0, 1)

        # button for opening new page
        newpagetab = QAction("+", self) 
        newpagetab.triggered.connect(lambda: pages.new_page(self, HOMEPAGE_URL))
        self.pagebar.addAction(newpagetab)




        self.addToolBar(self.pagebar)
        self.addToolBar(self.navbar)
        self.setCentralWidget(self.mwid)
        self.show()

        pages.new_page(self, HOMEPAGE_URL)

if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    ex = App()
    app.exec_()
