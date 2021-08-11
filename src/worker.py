from os import path
from src.temp import temp
from src.ui import label, confirm, fatal, selectzip, success
import src.zip as zip
import sys
from threading import Thread

# Get path of imagemagick
imagemagick = ""
if getattr(sys, 'frozen', False):
    imagemagick = path.dirname(sys.executable)
elif __file__:
    imagemagick = path.dirname(__file__)
    imagemagick = path.dirname(imagemagick[:-1])
imagemagick = path.join(imagemagick, 'imagemagick', 'convert.exe')

thread = None


def start():
    global thread
    if thread != None:
        thread.kill()
    Thread(target=convert).start()


def convert():
    # Check if app is in another process
    from subprocess import check_output
    from shutil import copy2
    s = check_output('tasklist', shell=True)
    if s.count(b"pymanga") > 1:
        fatal("Pymanga is already running on another process!")

    # Prompt for archive
    file = selectzip("Open archive to use:")

    # Extract and read pdf file
    files, skipped = zip.read(file)
    if len(skipped):
        confirm("The following files will not be included:", str(skipped))

    if confirm("Choose format", "Do you want to convert the .cbz to .pdf?") == "yes":

        label("Creating .pdf file...")
        command = [imagemagick]
        command.extend(files)

        # Add output file to command
        from pathlib import Path
        outFile = path.basename(file)
        if "." in outFile:
            outFile = outFile.split(".")[0]
        outFile = path.join(temp, outFile + ".pdf")
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

    else:

        label("Creating .cbz file...")

        # Choose output filename
        from pathlib import Path
        outFile = path.basename(file)
        if "." in outFile:
            outFile = outFile.split(".")[0]
        outFile = path.join(temp, outFile + ".cbz")

        # Copy all images in order to root of temp folder
        order = 0
        pages = []
        fill = len(str(len(files))) + 1
        for file in files:
            order += 1
            page = str(order).zfill(fill) + file[file.rfind('.'):]
            copy2(file, page)
            pages.append(page)

        # Create .cbz file
        zip.create(pages, outFile)

    # Save output file to Desktop or open with default editor
    outFile2 = path.join(Path.home(), "Desktop", path.basename(outFile))
    try:
        copy2(outFile, outFile2)
    except Exception as e:
        fatal("Error copying file!", e=e)

    success("File saved to the desktop successfully!")

    from os import _exit
    _exit(1)
