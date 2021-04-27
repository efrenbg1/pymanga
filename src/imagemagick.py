import os
import sys
import wget
from src.temp import temp, clean
from src.ui import label, p

download = 'https://download.imagemagick.org/ImageMagick/download/binaries/ImageMagick-7.0.11-9-portable-Q16-x86.zip'

path = ""
if getattr(sys, 'frozen', False):
    path = os.path.dirname(sys.executable)
elif __file__:
    path = os.path.dirname(__file__)
    path = os.path.dirname(path[:-1])
imagemagick = os.path.join(path, 'imagemagick')


def check():
    if not os.path.isfile(os.path.join(imagemagick, 'convert.exe')):
        clean()
        label("Downloading ImageMagick...")
        p.stop()
        os.chdir(temp)
        out = wget.download(download, out=temp, bar=_progress)
        print(out)
        p.start()


_lastprogress = 0


def _progress(current, total, width):
    global _lastprogress
    progress = int(100*current/total)
    if progress == _lastprogress:
        return
    increment = progress-_lastprogress
    p.step(increment)
    _lastprogress = progress

# print("Saving pdf as '" + os.path.basename(os.getcwd()) + ".pdf'")
# command.append(os.path.basename(os.getcwd()) + ".pdf")
# subprocess.run(command)
