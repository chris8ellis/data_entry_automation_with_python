#!/usr/bin/python3

import os

def getfiles():
    pdflist = [ f for root, dirs, files in os.walk('./') for f in files if f.endswith('.pdf') ]
    return pdflist
print(getfiles())
