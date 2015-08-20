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

import urllib.request, urllib.parse, urllib.error
import re
import os

#Function for downloading one card based on the set prefix+card number.  It constructs the appropriate URL to hit magiccards.info's .jpg for that card
#and saves it to a hard-coded local directory structure based on the code for the set.
def downloadCard(setname, cardnumber, cardname):
    #Operating System check, mac is Darwin...pc is...else!
    if(os.uname().sysname == "Darwin"):
        if(not os.path.exists("/Users/peter/Documents/Projects/MTG/Images/" + setname + "/")):
            os.mkdir("/Users/peter/Documents/Projects/MTG/Images/" + setname + "/")
    else:
        if(not os.path.exists("E:\\Magic Card Images\\" + setname + "\\")):
            os.mkdir("E:\\Magic Card Images\\" + setname + "\\")
    
    urllib.request.urlretrieve("http://magiccards.info/scans/en/"+setname+"/"+cardnumber+".jpg", "/Users/peter/Documents/Projects/MTG/Images/" + setname + "/" + cardnumber + ".jpg")
    return

#DownloadSet takes a set prefix and scrapes the english version of the directory listing for that set on magiccards.info.
#It enumerates the cards in the set, and calls downloadCard on each in turn to pull the card images to the local hard drive.
def downloadSet(setname):
    print(setname)
    setdata = urllib.request.urlopen("http://magiccards.info/"+setname+"/en.html")
    it = re.finditer(re.escape("<a href=\"/") + setname + re.escape("/en/") + "(\d*\w*)" + re.escape(".html\">") + "([^<]*)", str(setdata.read()))
    while True:
        try:
            value = next(it)
        except StopIteration:
            break
        cardnumber = value.group(1)
        cardname = value.group(2)
        downloadCard(setname, cardnumber, cardname)
    return

dir = urllib.request.urlopen("http://magiccards.info/sitemap.html")
data = dir.read()
toFind = re.escape("<small style=\"color: #aaa;\">") + "(\w*)" + re.escape("</small>")
#Use a regex to scrape the set prefixes out of the sitemap.
it = re.finditer(toFind, str(data))
while True:
    try:
        value = next(it)
    except StopIteration:
        break
    setname = value.group(1)
    #de is the indicator that we're over into german cards.  Stop at that point, I don't think there is much to gain by having all the foreign language versions at this point.
    if setname == "de":
         break
    #Skip en, it is the indicator that we're in the language section (the languages get flagged as "sets" too by the regex)
    #Otherwise, go ahead and grab the set
    if setname != "en":
        downloadSet(setname)
