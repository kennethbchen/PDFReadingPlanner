import fitz


filename = 'ignore/soci.pdf'

doc = fitz.open(filename)

beginning_offset = 41

ol = doc.outline


def get_internal_page(book_page):
    return book_page + 41


def get_outline_structure(outline, level=0):
    """ Gets the full tree structure of an outline.

    :param outline: Outline Object to get the layout of
    :param prefix: Prefix that shows the level of the outline
    leave blank for calling it

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

    :param outline_structure: Tree Structure of the outline
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


for item in get_parent_tree(get_outline_structure(ol), 82):
    print(str(item[0]) + " " + str(item[1]) + " " + item[2])

