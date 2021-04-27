#!/usr/bin/python3
from src import ui, imagemagick
from threading import Thread


thread = Thread(target=imagemagick.check).start()

ui.loop()
