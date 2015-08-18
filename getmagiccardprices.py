#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Geoff
#
# Created:     10/04/2012
# Copyright:   (c) Geoff 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys
import urllib
import csv
import re
import time

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

class Render(QWebPage):
  def __init__(self, url):
    self.app = QApplication(sys.argv)
    QWebPage.__init__(self)
    self.loadFinished.connect(self._loadFinished)
    self.mainFrame().load(QUrl(url))
    self.app.exec_()

  def _loadFinished(self, result):
    self.frame = self.mainFrame()
    self.app.quit()

#url = 'http://sitescraper.net'
#r = Render(url)
#html = r.frame.toHtml()


ifile  = open('C:\\Users\\Geoff\\Desktop\\mcardlist.csv', "rb")
ofile = open('C:\\Users\\Geoff\\Desktop\\py-mcardlist.csv', "a")
reader = csv.reader(ifile, delimiter=';')
pattern = re.compile("TCGPPriceLow\".*\$(\d*.\d\d).*TCGPPriceMid.*\$(\d*.\d\d).*TCGPPriceHigh[^\$]*\$(\d*.\d\d)")

counter = 0;

for row in reader:
    if counter < int(sys.argv[1]):
        counter = counter + 1
        continue

    cardurl = 'http://magiccards.info/query?q=!' + row[0]
    cardinfo = Render(cardurl)
    myhtml = unicode(cardinfo.frame.toHtml()).encode('ascii','ignore')
    #print myhtml
    prices = pattern.search(myhtml)
    toWrite = "\"" + row[0] + "\"," + row[1] + ","
    if prices:
        toWrite = toWrite + prices.group(1) + "," + prices.group(2) + "," + prices.group(3) + "," + str(float(prices.group(1)) * int(row[1])) + "," + str(float(prices.group(2)) * int(row[1])) + "," + str(float(prices.group(3)) * int(row[1]))
    else:
        toWrite = toWrite + ",,,,,"
    toWrite = toWrite + "\n"
    print toWrite
    ofile.write(toWrite)
    exit()