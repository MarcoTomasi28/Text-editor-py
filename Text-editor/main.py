from tkinter import *               #Tk
from tkinter import filedialog      #Tk
from tkinter import font            #Tk
from typing import TextIO           
import time                         #Clock
from time import strftime           #Clock
import pyttsx3                      #Text to speach

global background_color
background_color = "yellow"

root = Tk()
root.title('Text editor')
root.geometry("1200x650")

global open_status_name
global selected
global background_color_selected
global tts_rate
background_color_selected = StringVar()
background_color_selected.set("yellow")
open_status_name = False
tts_rate = 150


#new file function
def new_file():
    global open_status_name
    text_box.delete("1.0", END)
    root.title('New file - Text editor')
    status_bar.config(text="New file        ")
    open_status_name = False

#open file function
def open_file():
    text_box.delete("1.0", END)
    text_file = filedialog.askopenfilename(initialdir="", title="Open File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    
    if text_file:
        global open_status_name
        open_status_name = text_file

    name = text_file
    root.title(f'{name} - Text editor')
    status_bar.config(text=f'{name}        ')

    text_file = open(text_file, 'r', encoding="utf8")
    stuff = text_file.read()
    text_box.insert(END, stuff)
    text_file.close()

#save as file function
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if text_file:
        name = text_file
        root.title(f'{name} - Text editor')
        status_bar.config(text=f'Saved: {name}        ')
        global open_status_name
        open_status_name = text_file
        #save file
        text_file = open(text_file, 'w', encoding="utf8")
        text_file.write(text_box.get("1.0", END))
        text_file.close()
        

#save file function
def save_file(e):
    global open_status_name
    if open_status_name:
        text_file = open(str(open_status_name), 'w', encoding="utf8")
        text_file.write(text_box.get("1.0", END))
        text_file.close()
        status_bar.config(text=f'Saved: open_status_name        ')
    else:
        save_as_file()

#cut text function
def cut_text(e):
    global selected
    if e:
        selcted = root.clipboard_get()
    else:
        if text_box.selection_get():
            selected = text_box.selection_get()
            text_box.delete("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected)

#copy text function
def copy_text(e):
    global selected
    try:
        if e:
            selcted = root.clipboard_get()
        else:
            if text_box.selection_get():
                selected = text_box.selection_get()
                root.clipboard_clear()
                root.clipboard_append(selected)
    except:
        return

#paste text function
def paste_text(e):
    global selected
    try:
        if e:
            selected = root.clipboard_get()
        else:
            if selected != False:
                position = text_box.index(INSERT)
                text_box.insert(position, selected)
    except:
        return

#insert time function
def insert_time(e):
    position = text_box.index(INSERT)
    text_box.insert(position, strftime("%H:%M %Y-%m-%d"))

#select all
def select_all(e):
    text_box.tag_add(SEL, "1.0", END)
    text_box.mark_set(INSERT, "1.0")
    text_box.see(INSERT)
    return 'break'

#highlight color change
def highlight_color_change(background_color_selected):
    global background_color
    global root
    if background_color_selected.get() == "Yellow":
        background_color = "Yellow"
    elif background_color_selected.get() == "Blue":
        background_color = "#0a67d6"
    elif background_color_selected.get() == "Pink":
        background_color = "Pink"
    elif background_color_selected.get() == "Gray":
        background_color = "#9c9c9c"
    elif background_color_selected.get() == "Red":
        background_color = "Red"   
    root.update()
    text_box.tag_add("start", "1.0", END)
    text_box.tag_config("start", selectbackground=str(background_color))

#open customize menu
def open_customize_menu(e):
    global background_color_selected
    background_color_selected.set(background_color_selected.get())
    top = Toplevel(root)
    top.geometry("600x250")
    top.title("Customize")
    Label(top, text= "Highlight color").pack(pady=10)
    OptionMenu(top, background_color_selected, "Yellow", "Blue", "Pink", "Gray", "Red").pack()
    Button(top, text="Apply", command=lambda: highlight_color_change(background_color_selected)).pack(pady=10)
   
#start tts
def start_tts(e):
    global tts_rate
    engine = pyttsx3.init()
    text_tts = text_box.get("1.0", END)
    engine.setProperty('rate', int(tts_rate))
    engine.say(text_tts)
    engine.runAndWait()

#set tts speed
def set_tts_speed(text_box_tts_option):
    global tts_rate
    tts_speed_selected = text_box_tts_option.get("1.0", END)
    tts_rate = tts_speed_selected

#tts options
def options_tts(e):
    global tts_rate
    option_window = Toplevel(root)
    option_window.geometry("600x250")
    option_window.title("Text to speach options")
    Label(option_window, text= "Speed (1-400)").pack(pady=10)
    text_box_tts_option = Text(option_window, width=5, height=1)
    text_box_tts_option.pack()
    Button(option_window, text="Apply", command=lambda: set_tts_speed(text_box_tts_option)).pack(pady=10)

#excel formatter
def excel_formatter(e):
    startpos = "1.0"
    while True:
        pos = text_box.search("(", startpos, END)
        if not pos:
            break

        startpos = f"{pos}+1c"
        text_box.insert(startpos, "\n")

#test
def test():
    print("no test selected")


#main frame
main_frame = Frame(root)
main_frame.pack(pady=5)

#text box scroll bar
text_scroll = Scrollbar(main_frame)
text_scroll.pack(side=RIGHT, fill=Y)

#text horizontal scrolbar
hor_scroll = Scrollbar(main_frame, orient="horizontal")
hor_scroll.pack(side=BOTTOM, fill=X)

#text box
text_box = Text(main_frame, width=97, height=25, font=("Helvetica", 16), selectbackground=str(background_color), selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="none", xscrollcommand=hor_scroll.set)
text_box.pack()

#configure scroll bar
text_scroll.config(command=text_box.yview)
hor_scroll.config(command=text_box.xview)

#menu
main_menu = Menu(root)
root.config(menu=main_menu)

#file menu
file_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=lambda: save_file(False), accelerator="Ctrl+s")
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

#edit menu
edit_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="Ctrl+x")
edit_menu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="Ctrl+c")
edit_menu.add_command(label="Paste                    ", command=lambda: paste_text(False), accelerator="Ctrl+v")
edit_menu.add_separator()
edit_menu.add_command(label="Date and Time", command=lambda: insert_time(False), accelerator="F5")
edit_menu.add_command(label="Select all", command=lambda: select_all(False), accelerator="Ctrl+a")
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=text_box.edit_undo, accelerator="Ctrl+z")
edit_menu.add_command(label="Redo", command=text_box.edit_redo, accelerator="Ctrl+y")

#functions menu
functions_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Functions", menu=functions_menu)
functions_menu.add_command(label="Start text to speech", command=lambda: start_tts(False), accelerator="Ctrl+f2")
functions_menu.add_command(label="Text to speech options", command=lambda: options_tts(False))
functions_menu.add_command(label="Format excel formulas", command=lambda: excel_formatter(False))

#customize menu
customize_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Customize", menu=customize_menu)
customize_menu.add_command(label="Change appearance             ", command=lambda: open_customize_menu(False))
customize_menu.add_command(label="Test", command=lambda: test())

#bottom status bar
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

#bind keys
root.bind("<Control-x>", cut_text)
root.bind("<Control-c>", copy_text)
root.bind("<Control-v>", paste_text)
root.bind("<F5>", insert_time)
root.bind("<Control-s>", save_file)
root.bind("<Control-F2>", start_tts)

root.mainloop()