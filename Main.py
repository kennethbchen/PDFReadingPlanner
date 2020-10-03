import outline_script
import tkinter as tk
from tkinter import *
from tkinter import filedialog

# Window / Root
window = Tk()
window.title("PDF Reading Planner")


document_path = StringVar()
document_path_display = StringVar()
document_path_display.set("Open File...")

start_page = StringVar()
days = StringVar()
toc_offset = StringVar()
trim_by = StringVar()


def ask_for_file():
    global document_path
    global document_indicator
    temp = filedialog.askopenfilename()

    if temp is not "":
        document_path.set(temp)
        document_path_display.set(temp)


def verify_input():
    if document_path.get() is not "" and \
            all(v for v in [start_page.get().isnumeric(), days.get().isnumeric(),
                            toc_offset.get().isnumeric(), trim_by.get().isnumeric()]):
        return True
    else:
        return False


def print_all():
    print(document_path.get(), start_page.get(), days.get(), toc_offset.get(), trim_by.get())

def generate_plan():
    if verify_input():
        outline_script.generate_plan(document_path.get(), int(start_page.get()),
                                     int(days.get()), int(toc_offset.get()), int(trim_by.get()))
    else:
        print("uh uh")

# Main Frame
content = tk.Frame(window)
content.grid(column=0, row=0)


# Output
output_box = tk.Text(content, width=50, height=25)
output_box.grid(column=0, row=0, rowspan=6)


# Document Parameter
document_frame = tk.Frame(content, padx=5, pady=5)
document_frame.grid(column=1, row=0)

document_label = tk.Label(document_frame, text="Document")
document_label.grid(column=0, row=0, columnspan=2)

document_indicator = tk.Label(document_frame, justify="right", width=10, textvariable=document_path_display)
document_indicator.grid(column=0, row=1)

document_button = tk.Button(document_frame, text="Open File", command=ask_for_file)
document_button.grid(column=1, row=1)


# Start Page Parameter
start_page_frame = tk.Frame(content, padx=5, pady=5)
start_page_frame.grid(column=1, row=1)

start_page_label = tk.Label(start_page_frame, text="Start Page #")
start_page_label.grid(column=0, row=0)

start_page_input = tk.Entry(start_page_frame, width=5, justify="center", textvariable=start_page)
start_page_input.grid(column=0, row=1)


# Days parameter
days_frame = tk.Frame(content, padx=5, pady=5)
days_frame.grid(column=1, row=2)

days_label = tk.Label(days_frame, text="Days")
days_label.grid(column=0, row=0)

days_input = tk.Entry(days_frame, width=5, justify="center", textvariable=days)
days_input.grid(column=0, row=1)


# TOC Offset Parameter
toc_offset_frame = tk.Frame(content, padx=5, pady=5)
toc_offset_frame.grid(column=1, row=3)

toc_offset_label = tk.Label(toc_offset_frame, text="TOC Offset")
toc_offset_label.grid(column=0, row=0)

toc_offset_input = tk.Entry(toc_offset_frame, width=5, justify="center", textvariable=toc_offset)
toc_offset_input.grid(column=0, row=1)


# Trim-By Parameter
trim_by_frame = tk.Frame(content, padx=5, pady=5)
trim_by_frame.grid(column=1, row=4)

trim_by_label = tk.Label(trim_by_frame, text="Trim-By")
trim_by_label.grid(column=0, row=0)

trim_by_input = tk.Entry(trim_by_frame, width=5, justify="center", textvariable=trim_by)
trim_by_input.grid(column=0, row=1)

# Generate Button
document_button = tk.Button(content, text="Generate Plan", command=generate_plan)
document_button.grid(column=1, row=5)

window.mainloop()