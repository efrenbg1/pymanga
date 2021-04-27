from tkinter import messagebox, Label, Tk
from tkinter.ttk import Progressbar
import os
import sys
import traceback

title = "pymanga | .zip to .pdf"
spin = True

# Start window and set icon
root = Tk()
root.title(title)
path = ""
if getattr(sys, 'frozen', False):
    path = os.path.dirname(sys.executable)
elif __file__:
    path = os.path.dirname(__file__)
    path = os.path.dirname(path[:-1])
icon = os.path.join(path, 'app.ico')
root.iconbitmap(icon)
root.geometry("250x100")

_label = None

# Top space
tpre = Label(root, text='')
tpre.pack()

# Main text
t = Label(root, text="Cargando...", font=('helvetica', 12, 'bold'))
t.pack()
_label = t

# Spinner
p = Progressbar(root, length=200,
                mode="indeterminate", takefocus=True, maximum=100)
p.pack()
p.start()

# Bottom space
tpost = Label(root, text='')
tpost.pack()


def label(msg):
    _label.config(text=msg)


def loop():
    root.mainloop()


def fatal(msg, e=None):
    global spin
    spin = False
    if e != None:
        traceback.print_exc()
        msg += "\n\n" + str(e)
    messagebox.showerror(message=msg, title=title)
    os._exit(1)


def confirm(title, msg):
    global spin
    spin = False
    answer = messagebox.askquestion(title, msg, icon='question')
    spin = True
    return answer
