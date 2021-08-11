#!/usr/bin/python3
from src import ui, worker

ui.paint()

worker.start()

ui.loop()
