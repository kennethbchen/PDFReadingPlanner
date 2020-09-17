import fitz


filename = 'ignore/soci.pdf'
doc = fitz.open(filename)
ol = doc.outline
beginning_offset = 41


def get_internal_page(book_page):
    """
    Gets the internal page number based on the beginning_offset.
    This is needed because PDFs may number their pages starting later in the book.
    For example, the PDF may have a preface section which is not numbered in the same
    way as the table of contents. This means the table of contents won't match up with
    the actual page number in the PDF
    :param book_page: Page based on the table of contents to convert
    :return: converted page number
    """
    return book_page + beginning_offset


def get_outline_structure(outline, level=0):
    """ Gets the full tree structure of an outline.

    :param outline: Outline Object to get the layout of
    :param level: Prefix that shows the level of the outline. Leave blank

    :rtype [level <int>, page <int>, title <str>]
    :return: List that represents structure of the outline
    """
    output = []
    while outline is not None:
        temp = [level, outline.page, outline.title]
        output.append(temp)
        #output.append(prefix + " " + str(outline.page) + " " + outline.title)
        if outline.down is not None:
            output.extend(get_outline_structure(outline.down, level + 1))
        outline = outline.next
    return output


def get_outline_range(outline_structure, min_page, max_page):
    """
    Gets the outline structure of a specific page range.
    min_page and max_page is the page number based on the table of contents
    of the PDF

    :param outline_structure: List of the outline contents
    :param min_page: minimum page to be selected
    :param max_page: maximum page to be selected
    :return:
    """
    min_page = get_internal_page(min_page)
    max_page = get_internal_page(max_page)

    output = []
    for item in outline_structure:
        if min_page <= item[1] <= max_page:
            output.append(item)
    return output


def get_parent_tree(outline_structure, start):
    """
    Gets the outline structure of one branch starting at a page number
    start is the page number based on the table of contents of the PDF
    :param outline_structure: List of the outline contents
    :param start: the first page of the tree you want to select

    :rtype [level <int>, page <int>, title <str>]
    :return: List that represents structure of the outline range
    """
    start = get_internal_page(start)
    output = []
    max_level = -1

    for item in outline_structure:
        if item[1] == start - 1:
            output.append(item)
            max_level = item[0]
            continue

        if (item[1] >= start) and (item[0] > max_level):
            output.append(item)
        elif (len(output) > 0) and (item[0] == max_level):
            output.append(item)
            break

    return output

def get_page_counts(outline_structure):
    for val in range(0, len(outline_structure)):
        if val > 0:
            outline_structure[val - 1].append(outline_structure[val][1] - outline_structure [val - 1][1])

    del outline_structure[-1]
    return outline_structure



structure = get_page_counts(get_parent_tree(get_outline_structure(ol), 198))

# for val in structure:
#     print(val[2] + " [" + str(val[3]) + "p]")

def partition_outline(outline_structure, days):
    output = []
    buffer = []
    total_pages = 0
    for item in outline_structure:
        total_pages += item[3]
    pages_per_day = total_pages / days
    print(pages_per_day)
    count = 0
    for item in outline_structure:
        print(item)
        if (count + item[3]) <= pages_per_day:
            count += item[3]
            buffer.append(item)
        else:

            output.append(buffer)
            count = 0
            buffer = []


    if len(buffer) != 0:
        output.append(buffer)

    return output

for val in partition_outline(structure, 5):
    print(val)


#
# print("---------")
# for val in range(0, len(structure)):
#      print(str(structure[val][0]) + " " + str(structure[val][1] - beginning_offset + 1) + " " + str(structure[val][2]) + " " + str(structure[val][3]))


