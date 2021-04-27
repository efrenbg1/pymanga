import re
import os
import subprocess
from src.temp import temp

def _atoi(text):
    return int(text) if text.isdigit() else text


def _natural_keys(text):
    return [_atoi(c) for c in re.split(r'(\d+)', text)]


def read(file, pattern):
    subprocess.Popen(['tar', '-xf', file, '--directory', temp])
    os.chdir(temp)
    files = []
    skipped = []
    chapters = os.listdir()
    chapters.sort(key=_natural_keys)
    for chapter in chapters:
        if pattern == "None":
            if not chapter.isdecimal():
                skipped.append(chapter)
                continue
        else:
            if pattern not in chapter:
                skipped.append(chapter)
                continue

        pages = os.listdir(chapter)
        pages.sort(key=_natural_keys)
        for page in pages:
            if '.jpg' in page or '.png' in page:
                files.append(chapter + "/" + page)
            else:
                skipped.append(chapter + "/" + page)
