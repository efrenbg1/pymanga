from os import path
from src.temp import temp
from src.ui import label, confirm, fatal, selectzip
import src.zip as zip
import sys

# Get path of imagemagick
imagemagick = ""
if getattr(sys, 'frozen', False):
    imagemagick = path.dirname(sys.executable)
elif __file__:
    imagemagick = path.dirname(__file__)
    imagemagick = path.dirname(imagemagick[:-1])
imagemagick = path.join(imagemagick, 'imagemagick', 'convert.exe')


def convert():
    # Check if app is in another process
    from subprocess import check_output
    s = check_output('tasklist', shell=True)
    if s.count(b"pymanga") > 1:
        fatal("Pymanga is already running on another process!")

    # Prompt for archive
    command = [imagemagick]
    file = selectzip("Open archive to use:")

    # Extract and read pdf file
    files, skipped = zip.read(file)
    if len(skipped):
        confirm("The following files will not be included:", str(skipped))
    label("Creating pdf file...")
    command.extend(files)

    # Add output file to command
    from pathlib import Path
    outFile = path.basename(file)
    if "." in outFile:
        outFile = outFile.split(".")[0]
    outFile = path.join(temp, outFile + ".pdf")
    print(outFile)
    command.append(outFile)

    # Convert file using ImageMagick
    from subprocess import Popen, PIPE, STDOUT
    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, encoding='UTF8')

    # Wait for process to finish
    from time import sleep
    while p.poll() is None:
        sleep(1)
    response = p.stdout.readline()
    if response != "":
        fatal("Can't convert to pdf!", response)

    # Open pdf file with default editor
    if confirm("Save file", "Do you want to save the pdf to the Desktop?"):
        outFile2 = path.join(Path.home(), "Desktop", path.basename(outFile))
        from shutil import copy2
        try:
            copy2(outFile, outFile2)
        except Exception as e:
            fatal("Error copying file!", e=e)
    else:
        from os import startfile
        startfile(outFile, 'open')
    from os import _exit
    _exit(1)
