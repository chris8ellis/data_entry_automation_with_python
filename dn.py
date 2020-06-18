#!/usr/bin/python3

import os
from PyPDF2 import PdfFileReader
import pdfplumber

def getfiles():
    pdflist = [ root+"/"+f for root, dirs, files in os.walk('./') for f in files if f.endswith('.pdf') ]
    return pdflist

filename1 = 'formats/format1/folder/1900070.pdf'
filename2 = 'formats/format2/211559-050.pdf'
filename3 = 'Mar20.pdf'

def readini(fname):
    ini = open(fname, 'r')
    instructions = ini.read()
    ini.close()
    return instructions

"""
------------------------
 getfields with PyPDF2
------------------------
pdfFileObj = open(filename2,'rb')
pdfReader = PdfFileReader(pdfFileObj)

#print(pdfReader.getFields())
#texFields= pdfReader.gettextfields()
dict = pdfReader.getFields()

for field in dict:
    print(field)
"""

def getformfields(field):
    field_value = ""
    
    try:
        field_value = field.resolve()['V'].decode('utf-8')

    except:
        field_value = "NaN"

    return field_value

# get fields with pdfplumber
def getfields(fn):
    pdf = pdfplumber.open(fn)
    fields = pdf.doc.catalog["AcroForm"].resolve()["Fields"]
    #print(fields)

    form_data = {}

    for field in fields:
        try:
            field_name = field.resolve()['T'].decode('utf-8')
            field_value = getformfields(field)
        except:
            next
        form_data[field_name] = field_value
    pdf.close()
    return form_data

def gettextfields(fn):
    pdf = pdfplumber.open(fn)
    p0 = pdf.pages[0]
    """
    # using crop method - replaced with extract_table() method
    p0_crop = p0.within_bbox((30, 160, 160, 179))
    words = p0_crop.extract_words()
    deliveryDate = date[0]['text']
    deliveryNote = date[1]['text']
    """
    tab = p0.extract_table()
    deliveryDate = tab[1][0]
    deliveryNote = tab[1][1]
    pdf.close()
    return deliveryDate, deliveryNote



def execute():
    i1 = readini('format1.ini')
    i2 = readini('format2.ini')
        #print(i1)
        #print(i2)
        
    for file in getfiles():
        try:
            print(getfields(file))
            print(gettextfields(file))
        except:
            print("Error with file: " + file)
        
if __name__ == '__main__':    
    execute()

#print(getfields(filename1))

#pdf.close()
