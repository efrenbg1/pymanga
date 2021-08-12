from tkinter import messagebox, Label, Tk, simpledialog, filedialog
from tkinter.ttk import Progressbar
from os import path, _exit
import sys
import traceback

title = "pymanga | .zip to .cbz or .pdf"

# Start window and set icon
root = Tk()
root.title(title)
icon = ""
if getattr(sys, 'frozen', False):
    icon = path.dirname(sys.executable)
elif __file__:
    icon = path.dirname(__file__)
    icon = path.dirname(icon[:-1])
icon = path.join(icon, 'app.ico')
root.iconbitmap(icon)
root.geometry("250x100")

_label = None
_p = None


def paint():
    global _label, _p

    # Top space
    tpre = Label(root, text='')
    tpre.pack()

    # Main text
    t = Label(root, text="Loading...", font=('helvetica', 12, 'bold'))
    t.pack()
    _label = t

    # Spinner
    p = Progressbar(root, length=200,
                    mode="indeterminate", takefocus=True, maximum=100)
    p.pack()
    p.start()
    _p = p

    # Bottom space
    tpost = Label(root, text='')
    tpost.pack()


def label(msg):
    _label.config(text=msg)


def loop():
    root.mainloop()


def fatal(msg, e=None):
    global _p
    _p.stop()
    if e != None:
        traceback.print_exc()
        msg += "\n\n" + str(e)
    messagebox.showerror(message=msg, title=title)
    _exit(1)


def success(msg):
    global _p
    _p.stop()
    messagebox.showinfo(message=msg, title=title)
    _p.start()


def confirm(title, msg):
    global _p
    _p.stop()
    answer = messagebox.askquestion(title, msg, icon='question')
    _p.start()
    return answer


def ask(title, msg):
    global _p
    _p.stop()
    prompt = Tk()
    prompt.overrideredirect(1)
    prompt.withdraw()
    answer = simpledialog.askstring(title, msg, parent=prompt)
    prompt.destroy()
    _p.start()
    return answer


def selectzip(title):
    global _p
    _p.stop()
    from pathlib import Path
    from os.path import join
    answer = filedialog.askopenfilenames(title=title, initialdir=str(join(Path.home(), "Downloads")), filetypes=(
        ('Archive', '*.zip'),
        ('All files', '*.*')
    ))
    _p.start()
    return answer
