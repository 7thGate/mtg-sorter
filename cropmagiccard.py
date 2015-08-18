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
import Image

def main():
    img = Image.open("C:\\Users\\Geoff\\Downloads\\spread.jpg")
    print list(img.getdata())
    return

if __name__ == '__main__':
    main()
