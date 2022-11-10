import tld_check as tldc
import settings_
import urllib

settings = settings_.check()


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import PyQt5.QtWebEngineWidgets as webengwid
from PyQt5.QtWebEngineWidgets import QWebEngineView as webview

# now when the url is changed sync it with 
# url bar
def set_urlbar_url(self, url):
    urll = url
    if url == None:
        _url = self.browser.url().toString()
        self.browser_urlbar.setText(_url)
        urll = _url
    elif type(url) == type(QUrl()):
        self.browser_urlbar.setText(url.toString())
    else:
        self.browser_urlbar.setText(url)

    # history = ""

    # ...and save the URL to the history
    # if os.path.exists(f"{os.getcwd()}/history") == False:
    #     _f = open("history", "w+")
    #     _f.write("")
    #     _f.close()
    # else:
    #     _f = open("history", "r+")
    #     history = _f.read() 
    #     _f.close()

    # _hf = open("history", "w+")

    # history += "\n" + urll 

    # _hf.write(history) 
    # _hf.close()


# the code could just use self.browser.setUrl(), but 
# to comfortable use it some more ricing is needed
def go_to_url(self, url):
    urltg = url

    if url == None:
        urltg = self.browser_urlbar.text()


    # smart but dumb url tld checker
    tld_found = False

    urlog = urltg
    urlpq = self.BROWSER_SE + urllib.parse.quote(urlog)

    if not urlog.find(" ") > 0:
        for tld in tldc.TLD_DOMAINS:
            if urltg.casefold().find(f".{tld.casefold()}") > 0:
                if not urltg.startswith("https://"):
                    if not urltg.startswith("http://"):
                        urltg = "https://" + urltg
                tld_found = True
    
    else:
        urltg = urlpq
        
    if tld_found == False: urltg = urlpq

    self.browser.setUrl(QUrl(urltg))
    set_urlbar_url(self, urltg)

def switch_to_page(self, page):
    ppage = self.grlt.itemAt(0).widget() 
    self.prev_page = ppage
    ppage.setParent(None)

    self.browser = page
    self.grlt.addWidget(page, 0, 0, 0, 0)
    set_urlbar_url(self, page.url().toString())

# set its title
def set_page_title(self, page, acitem):
    title = page.title()
    _title = title

    maxlen = settings.get("misc").get("max_page_title_length")

    if len(title) > maxlen:
        title = ""
        for i in range(maxlen):
            title += _title[i]

    acitem.setText(title)

# and close the page
# (yeah...)
def close_page(self, acitem, acitemicon, closebtn, page):
    page.close()
    page.setParent(None) 

    ppage = self.prev_page
    self.browser = ppage 
    self.grlt.addWidget(ppage, 0, 0, 0, 0)
    
    self.pagebar.removeAction(acitemicon)
    self.pagebar.removeAction(acitem)
    self.pagebar.removeAction(closebtn)

# create new page
def new_page(self, url):
    page = webview()
    if url == None:
        url = HOMEPAGE_URL
    else: url = QUrl(url)

    page.setUrl(url)

    self.grlt.itemAt(0).widget().setParent(None) 
    self.prev_page = page
    self.browser = page
    self.grlt.addWidget(page, 0, 0, 0, 0)
    
    acitem = QAction(url.toString())
    page.titleChanged.connect(lambda: set_page_title(self, page, acitem))

    acitemicon = QAction("")
    page.iconChanged.connect(lambda: acitemicon.setIcon(page.icon()))


    acitem.triggered.connect(lambda: switch_to_page(self, page))
    acitemicon.triggered.connect(lambda: switch_to_page(self, page))

    set_urlbar_url(self, url.toString())

    # closebtn = QAction("-X|")
    closebtn = QAction("ⓧ")
    closebtn.triggered.connect(lambda: close_page(self, acitem, acitemicon, closebtn, page)) 

    self.pagebar.addAction(acitemicon)
    self.pagebar.addAction(acitem)
    self.pagebar.addAction(closebtn)

    # on url changed / on title changed
    page.urlChanged.connect(lambda: set_urlbar_url(self, None))
    page.titleChanged.connect(lambda: self.setWindowTitle(self.browser.title() + " - UCI Browser"))