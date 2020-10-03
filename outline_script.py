import fitz
from math import ceil
import tkinter


def get_outline_structure(outline, level=0):
    """ Gets the full structure of an outline.

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

    # The partition is just a list with numbers representing how many sections to read goes in that group.
    # For example [4,5] means that in a list of all the sections, the first four go in group 1 and the rest in group 2
    return output


def assemble_output(partition, section_levels, section_titles, section_start_pages, section_page_counts):
    output = []

    slice_start = 0
    for i in range(0, len(partition)):
        temp = []
        for j in range(slice_start, slice_start + partition[i]):
            temp_section = [section_levels[j], section_titles[j], section_start_pages[j], section_page_counts[j]]
            temp.append(temp_section)
        output.append(temp)
        slice_start += partition[i]
    return output


def generate_plan(file_path, toc_start_page, days, toc_offset=0, trim_by=0, debug=False):
    ol = fitz.open(file_path).outline

    # Get only the headings that we want
    headings = get_parent_tree(get_outline_structure(ol), toc_start_page + toc_offset)

    for i in range(0, trim_by):  # Remove a certain number of the headings from the back
        headings.pop(-1)

    # Separate headings into three lists
    levels, section_start_pages, section_titles = zip(*headings)

    section_page_counts = get_page_counts(section_start_pages)

    pages_per_day = ceil(sum(section_page_counts) / days)

    partition = partition_outline(section_page_counts, pages_per_day)

    plan = assemble_output(partition, levels, section_titles, section_start_pages, section_page_counts)
    # TODO Sift Algorithm
    if debug:
        print("levels:", levels)
        print("section start pages:", section_start_pages)
        print("section titles:", section_titles)
        print("section page counts", section_page_counts)
        print("ppd", pages_per_day)
        print("partition", partition)
        print(plan)

        print("Pages/Day: " + str(pages_per_day))
        for val in plan:

            for item in val:
                for count in range(0, item[0]):
                    print("  ", end='')
                print(item[1] + " [" + str(item[2]) + "; " + str(item[3]) + "p]\n")
            print("----------------------------------------------------------")

    output = ""
    output += "Pages/Day: " + str(pages_per_day) + "\n"
    for val in plan:

        for item in val:
            for count in range(0, item[0]):
                output += "  "
            output += item[1] + " [" + str(item[2]) + "; " + str(item[3]) + "p]\n"
        output += "----------------------------------------------------------\n"
    return output


