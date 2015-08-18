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

for root, dirs, files in os.walk("E:\\Magic Card Images\\"):
    if len(dirs) > 0:
        for dir in dirs:
            data = urllib.urlopen("http://magiccards.info/"+dir+"/en.html")
            lines = data.read().split("\n")
            state = 0
            cardinfo = []
            for line in lines:
                if state == 4:
                    featureFile = "E:\\Magic Card Images\\" + dir + "\\" + cardinfo[0] + ".dat"
                    file = open(featureFile, 'w')
                    for item in cardinfo:
                        file.write(item + "\n")
                    print cardinfo
                    cardinfo = []
                    state = 0
                elif state != 0:
                    line = line.lstrip().rstrip()
                    line = line.lstrip("<td")
                    line = line.lstrip(">")
                    line = line.rstrip("/td>")
                    line = line.rstrip("<")
                    line = cardinfo.append(line)
                    state = state + 1
                else:
                    it = re.finditer(re.escape("<a href=\"/") + dir + re.escape("/en/") + "(\d*\w*)" + re.escape(".html\">") + "([^<]*)", line)
                    try:
                        value = it.next()
                    except StopIteration:
                        continue
                    cardnumber = value.group(1)
                    cardname = value.group(2)
                    cardinfo.append(cardnumber)
                    cardinfo.append(cardname)
                    state = 1


