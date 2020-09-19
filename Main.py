import fitz
from math import ceil


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
        if outline.down is not None:
            output.extend(get_outline_structure(outline.down, level + 1))
        outline = outline.next
    return output


def get_parent_tree(outline_structure, internal_start_page):
    """
    Gets the outline structure of one branch starting at a page number
    start is the page number based on the table of contents of the PDF
    :param outline_structure: List of the outline contents
    :param internal_start_page: the first page of the tree you want to select

    :rtype [level <int>, page <int>, title <str>]
    :return: List that represents structure of the outline range
    """

    output = []
    max_level = -1

    for item in outline_structure:
        if item[1] == internal_start_page - 1:
            output.append(item)
            max_level = item[0]
            continue

        if (item[1] >= internal_start_page) and (item[0] > max_level):
            output.append(item)
        elif (len(output) > 0) and (item[0] == max_level):
            output.append(item)
            break

    return output


def get_page_counts(outline_structure):
    for val in range(0, len(outline_structure)):
        if val > 0:
            outline_structure[val - 1].append(outline_structure[val][1] - outline_structure[val - 1][1])

    del outline_structure[-1]  # We got one extra heading in order to do page count so remove it
    return outline_structure


def partition_outline(outline_structure, days):
    output = []
    buffer = []
    total_pages = 0
    for item in outline_structure:
        total_pages += item[3]
    pages_per_day = ceil(total_pages / days)
    count = 0
    for item in outline_structure:
        if (count + item[3]) <= pages_per_day:
            count += item[3]
            buffer.append(item)
        else:
            output.append(buffer)
            buffer = [item]
            count = item[3]

    if len(buffer) != 0:
        output.append(buffer)

    return pages_per_day, output


def generate_plan(document, toc_start_page, days, toc_offset=0, trim_by=0):
    ol = document.outline
    headings = get_page_counts(get_parent_tree(get_outline_structure(ol), toc_start_page + toc_offset))
    for i in range(0,trim_by):
        headings.pop(-1)

    pages_per_day, partition = partition_outline(headings, days)
    return pages_per_day, partition


filename = 'ignore/soci.pdf'
doc = fitz.open(filename)

rate, plan = generate_plan(doc, 250, 5, 41, 2)

print(rate)
for val in plan:
    print(val)
