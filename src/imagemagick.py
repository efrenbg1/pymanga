from os import path, startfile, _exit, getcwd
from subprocess import Popen, PIPE, STDOUT
from src.temp import temp
from src.ui import label, confirm, fatal
import src.zip as zip
from time import sleep
import sys

imagemagick = ""
if getattr(sys, 'frozen', False):
    imagemagick = path.dirname(sys.executable)
elif __file__:
    imagemagick = path.dirname(__file__)
    imagemagick = path.dirname(imagemagick[:-1])
imagemagick = path.join(imagemagick, 'imagemagick', 'convert.exe')


def convert(file):
    command = [imagemagick]
    files, skipped = zip.read(file)
    if len(skipped):
        confirm("The following files will not be included:", str(skipped))
    label("Creating .pdf file...")
    command.extend(files)
    outFile = path.join(temp, path.basename(getcwd()) + ".pdf")
    command.append(outFile)
    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, encoding='UTF8')
    while p.poll() is None:
        sleep(1)
    response = p.stdout.readline()
    if response != "":
        fatal("Can't convert to pdf!", response)
    startfile(outFile, 'open')
    _exit(1)
