#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Geoff
#
# Created:     26/02/2012
# Copyright:   (c) Geoff 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import urllib
import re
import os

def downloadCard(setname, cardnumber, cardname):
    if(not os.path.exists("E:\\Magic Card Images\\" + setname + "\\")):
        os.mkdir("E:\\Magic Card Images\\" + setname + "\\")
    urllib.urlretrieve("http://magiccards.info/scans/en/"+setname+"/"+cardnumber+".jpg", "E:\\Magic Card Images\\" + setname + "\\" + cardnumber + ".jpg")
    return

def downloadSet(setname):
    print(setname)
    setdata = urllib.urlopen("http://magiccards.info/"+setname+"/en.html")
    it = re.finditer(re.escape("<a href=\"/") + setname + re.escape("/en/") + "(\d*\w*)" + re.escape(".html\">") + "([^<]*)", str(setdata.read()))
    while True:
        try:
            value = it.next()
        except StopIteration:
            break
        cardnumber = value.group(1)
        cardname = value.group(2)
        downloadCard(setname, cardnumber, cardname)
    return

dir = urllib.urlopen("http://magiccards.info/sitemap.html")
data = dir.read()
toFind = re.escape("<small style=\"color: #aaa;\">") + "(\w*)" + re.escape("</small>")
it = re.finditer(toFind, str(data))
while True:
    try:
        value = next(it)
    except StopIteration:
        break
    setname = value.group(1)
    if setname == "de":
        break
#    if setname != "en":
#        downloadSet(setname)