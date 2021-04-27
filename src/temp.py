import os
import tempfile
from src.ui import fatal, label

try:
    temp = os.path.join(tempfile.gettempdir(), "pymanga")
    if not os.path.exists(temp):
        os.makedirs(temp)
    print(temp)
except Exception as e:
    fatal("No se puede abrir el directorio temporal:", e=e)


def clean():
    label("Limpiando archivos viejos...")
    for f in os.listdir(temp):
        f = os.path.join(temp, f)
        try:
            os.remove(f)
        except:
            pass
