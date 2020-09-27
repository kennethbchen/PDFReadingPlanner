import fitz
from math import ceil
import tkinter


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


def get_page_counts(section_pages):
    output = []
    for val in range(1, len(section_pages)):
        output.append(section_pages[val] - section_pages[val - 1])

    return output


def partition_outline(page_counts, pages_per_day):
    output = []
    buffer = []

    page_tally = 0
    section_count = 0
    for item in page_counts:

        if (page_tally + item) <= pages_per_day:
            page_tally += item
            section_count += 1
        else:
            output.append(section_count)
            section_count = 1
            page_tally = item

    if section_count != 1:
        output.append(section_count)

    return output


def slice_page_counts(partition, page_counts):
    output = []
    for item in partition:
        output.append(page_counts[:item])
        del page_counts[:item]
    return output


def generate_plan(document, toc_start_page, days, toc_offset=0, trim_by=0):
    ol = document.outline

    # Get only the headings that we want
    headings = get_parent_tree(get_outline_structure(ol), toc_start_page + toc_offset)
    for i in range(1, trim_by):  # Remove a certain number of the headings from the back
        headings.pop(-1)  # TODO Check this to make sure outlines are being selected properly, chapter 8 was in headings

    levels, heading_start_pages, section_titles = zip(*headings)
    print("levels:", levels)
    print("section bookmarks:", heading_start_pages)
    print("section titles:", section_titles)

    section_page_counts = get_page_counts(heading_start_pages)
    print("section page counts", section_page_counts)

    pages_per_day = ceil(sum(section_page_counts) / days)
    print("ppd", pages_per_day)

    partition = partition_outline(section_page_counts, pages_per_day)
    print("partition", partition)

    grouped_pages = slice_page_counts(partition, section_page_counts)
    print("group", grouped_pages)

    plan = []
    return pages_per_day, plan


filename = 'ignore/soci.pdf'
doc = fitz.open(filename)

rate, plan = generate_plan(doc, 250, 5, 41, 3) #294


# print("Pages/Day: " + str(rate))
# for val in plan:
#
#     for item in val:
#         for count in range(0, item[0]):
#             print("\t", end='')
#         print(item[2] + " [" + str(item[1]) + "; " + str(item[3]) + "p]\r")
#     print("----------------------------------------------------------")
