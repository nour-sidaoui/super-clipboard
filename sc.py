from tkinter import *
import pyperclip

copied_items = []


def detect_copy():
    global copied_items
    copied = "".join([c for c in pyperclip.paste() if ord(c) <= 65535])  # filtering non-tcl characters

    if copied not in copied_items and copied != '':
        copied_items.append(copied)
        add_new_clips()

    root.after(ms=200, func=detect_copy)


def replace_with_new_canvas():
    for child in my_canvas.winfo_children():
        child.destroy()


def add_new_clips():
    global copied_items
    max_slots = max_slots_scale.get()

    my_canvas.grid(row=1, column=0, padx=5, pady=3)  # packing here to avoid display if clipboard is empty

    if len(copied_items) > max_slots:
        copied_items = copied_items[-max_slots:]

    replace_with_new_canvas()
    for c in reversed(copied_items):
        item = Button(my_canvas,
                      width=50,
                      text=c,
                      padx=5,
                      pady=5,
                      relief=GROOVE,
                      wraplength=450,
                      fg='black',
                      justify=LEFT)
        item.pack(fill=X, side=BOTTOM)
        item.bind("<Button-1>", lambda event, label_content=item: on_click(label_content))

    if len(copied_items) == 0:
        item = Label(my_canvas,
                     text='- Clipboard is empty -',
                     font='Calibri 12 italic',
                     width=51,
                     padx=5,
                     pady=5,
                     relief=GROOVE,
                     bg='gray93',
                     fg='black',
                     wraplength=500,
                     justify=CENTER)
        item.pack(fill=X, side=BOTTOM)


def on_click(label_elem):
    label_text = label_elem["text"]
    pyperclip.copy(label_text)


def clear_last():
    try:
        on_click(my_canvas.winfo_children()[1])
        del copied_items[-1]
        add_new_clips()
    except IndexError:
        pass


def clear_all():
    global copied_items
    pyperclip.copy('')
    copied_items = []
    add_new_clips()


def on_top():
    if var.get() is True:
        root.wm_attributes("-topmost", "true")
    else:
        root.wm_attributes("-topmost", "false")
    root.update()


if __name__ == '__main__':
    root = Tk()
    root.title('Super Clipboard')
    root.config(bg='gray70')
    root.resizable(False, False)

    frame1 = Frame(root, borderwidth=5, relief=GROOVE, bd=1)
    frame1.grid_rowconfigure(0, weight=1)
    frame1.grid_columnconfigure(0, weight=1)

    # Buttons and Scale
    clear_mem = Button(frame1,
                       text='Clear clipboard',
                       padx=1,
                       command=clear_all,
                       width=15)

    clear_last = Button(frame1,
                        text='Clear last copy',
                        padx=1,
                        command=clear_last,
                        width=15)

    max_slots_scale = Scale(frame1,
                            from_=2,
                            to=8,
                            orient=HORIZONTAL,
                            label='Max number of slots',
                            length=140)

    var = BooleanVar()

    on_top = Checkbutton(frame1,
                         text="Keep on top ",
                         # variable=var,
                         command=on_top)

    # packing
    frame1.grid(row=0, column=0, sticky=EW, padx=5, pady=2)
    clear_mem.grid(row=0, column=0, pady=5)
    clear_last.grid(row=1, column=0, pady=5)
    max_slots_scale.grid(row=0, column=1, padx=15, pady=5, rowspan=2)
    on_top.grid(row=0, column=2, rowspan=2, sticky=E)

    max_slots_scale.set(5)

    my_canvas = Canvas(root)  # packed in add_new_clips() to display only if clipboard is non-0

    detect_copy()
    root.mainloop()