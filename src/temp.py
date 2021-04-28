from os import path
from tempfile import gettempdir
from src.ui import fatal, label

temp = path.join(gettempdir(), "pymanga\\")

def clean():
    from shutil import rmtree
    label("Cleaning temp directory...")
    try:
        rmtree(temp)
    except Exception as e:
        if type(e) != FileNotFoundError:
            fatal("Can't access temp directory!", e=e)
        pass
