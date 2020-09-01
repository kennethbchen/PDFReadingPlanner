import fitz

filename = 'soci.pdf'

doc = fitz.open(filename)

beginning_offset = 40


def select_pages(document, min_page, max_page, offset):
    """Selects a specific page range
    :param document PDF document
    :type document: <class 'fitz.fitz.document>

    :param min_page minimum page number to select (inclusive)
    :type <class Integer>

    :param max_page maximum page number to select (inclusive)
    :type <class Integer>

    :param offset number of introductory pages (stuff that's in roman numerals)
    required to make the min and max pages work properly
    :type <class Integer>

    :rtype [page]
    :return list of <class 'fits.fits.Page'> objects

    """
    return doc.pages(offset + min_page, offset + max_page)


def fonts(pages, granularity=False):
    """Extracts fonts and their usage in PDF documents.

    :param pages: Pages to iterate through
    :type pages: <class 'fitz.fitz.Page'>

    :param granularity: also use 'font', 'flags' and 'color' to discriminate text
    :type granularity: bool

    :rtype: [(font_size, count), (font_size, count}], dict
    :return: most used fonts sorted by count, font style information
    """


for page in select_pages(doc, 5, 6, beginning_offset):

    print(page.getTextPage().extractText())
