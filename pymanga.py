#!/usr/bin/python3
from subprocess import check_output
from src import ui, imagemagick
from threading import Thread
from os import _exit


ui.paint()


s = check_output('tasklist', shell=True)
if b"pymanga" in s:
    ui.fatal("Pymanga is already running on another process!")

thread = Thread(target=imagemagick.convert).start()

ui.loop()
