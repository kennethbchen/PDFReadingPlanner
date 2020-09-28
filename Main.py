import tkinter as tk
from tkinter import *



window = Tk()
window.title("PDF Reading Planner")

content = tk.Frame(window)

outline_box = tk.Text(content, width=50, height=25)

outline_separator = tk.Frame(content,height=20, relief="sunken")

output_box = tk.Text(content, width=50, height=25)

test = tk.Label(content, text="Please Help")

content.grid(column=0, row=0)
outline_box.grid(column=0, row=0, columnspan=1)
outline_separator.grid(column=0, row=1)
output_box.grid(column=0, row=2)
test.grid(column=1, row=0)

# left_frame = tk.Frame(content, borderwidth=1, relief="solid", width=200, height=100)
# left_frame.grid(column=0, row=0, columnspan=3, rowspan=2)

# label = tk.Label(text="Outline Structure")

#
# structure_box = tk.Text(width=25)
# structure_box.pack(side="left")

window.mainloop()