#!/usr/bin/python3
from src import ui, imagemagick
from threading import Thread
import sys

ui.paint()

thread = Thread(target=imagemagick.convert, args=(sys.argv[1], )).start()

ui.loop()
