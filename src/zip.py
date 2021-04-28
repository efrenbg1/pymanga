import re
from os import chdir, listdir
from zipfile import ZipFile
from src.temp import temp, clean
from src.ui import ask, fatal, label


def _atoi(text):
    return int(text) if text.isdigit() else text


def _natural_keys(text):
    return [_atoi(c) for c in re.split(r'(\d+)', text)]


def _extract(file):
    clean()
    label("Extracting archive...")
    archive = ZipFile(file)
    password = ""
    while True:
        try:
            archive.extractall(temp, pwd=bytes(password, 'utf-8'))
            break
        except Exception as e:
            print(e)
            password = ask("Password", "The file is encrypted and needs a password:")
            print(password)
            if password == None:
                fatal("Password is needed to extract archive!")
            pass


def read(file):
    try:
        _extract(file)
    except Exception as e:
        fatal("Can't open archive file!", e=e)

    chdir(temp)
    for folder in listdir():
        if folder in file:
            chdir(folder)

    files = []
    skipped = []
    chapters = listdir()
    chapters.sort(key=_natural_keys)
    for chapter in chapters:
        pages = listdir(chapter)
        pages.sort(key=_natural_keys)
        for page in pages:
            if '.jpg' in page or '.png' in page:
                files.append(chapter + "/" + page)
            else:
                skipped.append(chapter + "/" + page)

    return files, skipped
