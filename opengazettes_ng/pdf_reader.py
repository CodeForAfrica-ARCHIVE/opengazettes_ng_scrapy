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
    """
    Downloads the pdf from the given url, reads it and obtains the vol and no
    values
    :param url: URL from where to download the pdf
    :type url: string
    :return:
    :rtype:
    """
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

    vol = get_vol(text)
    no = get_no(text)
    return vol, no


def get_vol(data):
    """ Get Vol (Volume) value from data """
    vol = re.search("[^a-zA-Z](v\s*o\s*l\s*\.?\s*[^a-zA-Z\n,]+)",
                    data, re.IGNORECASE)
    # Check if the search result contains at least a digit
    if has_num(vol.group()):
        return ''.join([num for num in vol.group() if num.isdigit()])
    return '(nf)'


def get_no(data):
    """ Get No (Number) value from data """
    no = re.search("[^a-zA-Z](n\s*o\s*\.?\s*[^a-zA-Z\n,]+)",
                   data, re.IGNORECASE)
    # Check if the search result contains at least a digit
    if has_num(no.group()):
        return ''.join([num for num in no.group() if num.isdigit()])
    return '(nf)'


def has_num(text):
    """ Check if the string contains a digit """
    return any(str.isdigit(c) for c in text)
