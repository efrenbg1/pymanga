#!/usr/bin/python3

import os
import subprocess
import re
import sys

if len(sys.argv) < 2:
    print("Please specify string that chapter's folders must contain ('None' for folders named with only integers)")
    exit()


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


caps = os.listdir()
caps.sort(key=natural_keys)

command = ["convert"]
for cap in caps:
    if sys.argv[1] == "None":
        if not cap.isdecimal():
            print("Skipping " + cap + "...")
            continue
    else:
        if sys.argv[1] not in cap:
            print("Skipping " + cap + "...")
            continue

    pages = os.listdir(cap)
    pages.sort(key=natural_keys)
    for page in pages:
        if '.jpg' in page or '.png' in page:
            command.append(cap + "/" + page)
        else:
            print("Skipping " + cap + "/" + page + "...")

if len(command) == 1:
    print("No files found to convert!")
    exit()

print("Saving pdf as '" + os.path.basename(os.getcwd()) + ".pdf'")
command.append(os.path.basename(os.getcwd()) + ".pdf")
subprocess.run(command)
