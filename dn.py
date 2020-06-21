#!/usr/bin/python3

import os
from PyPDF2 import PdfFileReader
import pdfplumber

def getfiles():
    pdflist = [ root+"/"+f for root, dirs, files in os.walk('.') for f in files if f.endswith('.pdf') ]
    return pdflist

filename1 = 'formats/format1/folder/1900070.pdf'
filename2 = 'formats/format2/211559-050.pdf'
filename3 = 'Mar20.pdf'

def readini(fname):
    ini = open(fname, 'r')
    instructions = ini.read()
    iniList = instructions.split('\n')
    ini.close()
    return iniList

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

def createScript(fn, fieldValues, textValues):
    try:
        format_js = (
        f"document.getElementById('DeliveryDate').value = '{textValues[0]}'\n"
        f"document.getElementById('DeliveryNote').value = '{textValues[1]}'\n"
        f"document.getElementById('Ref1').value = '{fieldValues['Ref1']}'\n"
        f"document.getElementById('Desc1').value = '{fieldValues['Desc1']}'\n"
        f"document.getElementById('Qty1').value = '{fieldValues['Qty1']}'\n"
        f"document.getElementById('Pr1').value = '{fieldValues['Pr1']}'\n"
        f"document.getElementById('Amt1').value = '{fieldValues['Amt1']}'\n"
        f"document.getElementById('Ref2').value = '{fieldValues['Ref2']}'\n"
        f"document.getElementById('Desc2').value = '{fieldValues['Desc2']}'\n"
        f"document.getElementById('Qty2').value = '{fieldValues['Qty2']}'\n"
        f"document.getElementById('Pr2').value = '{fieldValues['Pr2']}'\n"
        f"document.getElementById('Amt2').value = '{fieldValues['Amt2']}'\n"
        )
        
    except:
        format_js =  (
        f"function selectedIdx(s, v) {'{'}\n"
        f"  for (var i = 0; i < s.options.length; i++) {'{'}\n"
        f"    if (s.options[i].text == v) {'{'}\n"
        f"      s.options[i].selected = true;\n"
        f"    return;\n"
        f"    {'}'}\n"
        f"{'  }'}\n"
        f"{'}'}\n"
        f"\n"
        f"document.getElementById('OR1').value = '{fieldValues['OR1']}'\n"
        f"document.getElementById('REF1').value = '{fieldValues['REF1']}'\n"
        f"document.getElementById('QUAN1').value = '{fieldValues['QUAN1']}'\n"
        f"document.getElementById('OR2').value = '{fieldValues['OR2']}'\n"
        f"document.getElementById('REF2').value = '{fieldValues['REF2']}'\n"
        f"document.getElementById('QUAN2').value = '{fieldValues['QUAN2']}'\n"
        f"document.getElementById('DES1').value = '{fieldValues['DES1']}'\n"
        f"selectedIdx(document.getElementById('CON1'), '{fieldValues['CON1']}');\n"
        f"document.getElementById('DES2').value = '{fieldValues['DES2']}'\n"
        f"selectedIdx(document.getElementById('CON2'), '{fieldValues['CON2']}');\n"

        )

    else:
        print("Format not recognized")
        
    newFile = open(fn+'.txt', 'w')
    newFile.write(format_js)
    newFile.close()

def execute():
    i1 = readini('format1.ini')
    i2 = readini('format2.ini')
    fileslist = getfiles()

    for file in fileslist:
        name = file.replace(".pdf","").split('/')[-1]

        try:
            field_vals = getfields(file)
            print(field_vals)
            text_vals = gettextfields(file)
            print(text_vals)
            createScript(name, field_vals, text_vals)
        except:
            print("Error with file: " + file)

if __name__ == '__main__':    
    execute()
