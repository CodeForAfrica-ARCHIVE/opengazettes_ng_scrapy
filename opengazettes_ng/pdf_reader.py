from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
import urllib2
from urllib2 import Request
from pdfminer.pdfparser import PDFParser
import re


def parse_pdf(url):
    pdf_data = urllib2.urlopen(Request(url)).read()
    # Cast to StringIO object
    from StringIO import StringIO
    memory_file = StringIO(pdf_data)

    # Create a PDF parser object associated with the StringIO object
    parser = PDFParser(memory_file)

    # Create a PDF document object that stores the document structure
    document = PDFDocument(parser)

    # Define parameters to the PDF device object
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    pageno = 1
    codec = 'utf-8'

    # Create a PDF device object
    device = TextConverter(rsrcmgr, retstr, codec=codec, pageno=pageno,
                           laparams=laparams)

    # Create a PDF interpreter object
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Process each page contained in the document
    text = ''
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        text = retstr.getvalue()

    vol = get_no(text)
    no = get_no(text)
    return vol, no


def get_vol(data):
    vol = re.search("\W(n\s*o\s*\.?\s*[0-9,\s*]+)", data, re.IGNORECASE)
    return vol


def get_no(data):
    no = re.search("\W(v\s*o\s*l\s*\.?\s*[0-9,\s*]+)", data, re.IGNORECASE)
    return no
