import csv
import json
from pathlib import Path

# Ruta absoluta a la carpeta data/ (raíz del proyecto), sin importar desde dónde se ejecute pytest
CARPETA_DATOS = Path(__file__).resolve().parent.parent / "data"


def leer_json(nombre_archivo):
    """Lee un archivo JSON de la carpeta data/ y devuelve su contenido (dict o list)."""
    ruta = CARPETA_DATOS / nombre_archivo
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


def leer_csv(nombre_archivo):
    """Lee un CSV de la carpeta data/ y devuelve una lista de diccionarios (un dict por fila)."""
    ruta = CARPETA_DATOS / nombre_archivo
    with open(ruta, encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))