from src.temp import temp, clean
from src.ui import ask, fatal, label


def _atoi(text):
    return int(text) if text.isdigit() else text


def _natural_keys(text):
    import re
    return [_atoi(c) for c in re.split(r'(\d+)', text)]


def _extract(file):
    # Extract zip file (if fails prompt for password)
    label("Extracting archive...")
    from zipfile import ZipFile
    archive = ZipFile(file)
    password = ""
    while True:
        try:
            output = temp + file[file.rfind('/')+1:file.rfind('.')]
            archive.extractall(output, pwd=bytes(password, 'utf-8'))
            break
        except:
            password = ask("Password", "The file is encrypted and needs a password:")
            if password == None:
                fatal("Password is needed to extract archive!")
            pass


def read(files):
    # Clean temp directory
    clean()

    for file in files:
        try:
            _extract(file)
        except Exception as e:
            fatal("Can't open archive file!", e=e)

    try:
        # Find extracted folder
        from os import chdir, listdir
        chdir(temp)

        # Get list of files to include (and those ignored)
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

    except Exception as e:
        fatal("Can't read contents of archive file!", e=e)


def create(files, out):
    from zipfile import ZipFile
    archive = ZipFile(out, 'w')

    for file in files:
        archive.write(file)

    archive.close()
