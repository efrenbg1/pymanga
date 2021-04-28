#!/usr/bin/python3
from src import ui, imagemagick
from threading import Thread

ui.paint()

thread = Thread(target=imagemagick.convert).start()

ui.loop()
