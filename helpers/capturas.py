import re
from datetime import datetime
from pathlib import Path

# Carpeta screenshots/ en la raíz del proyecto
CARPETA_CAPTURAS = Path(__file__).resolve().parent.parent / "screenshots"


def guardar_captura(driver, nombre_test):
    """Guarda una captura de pantalla en screenshots/ y devuelve su ruta.

    El nombre incluye el test y la fecha/hora, por ejemplo:
    test_login_invalido_usuario_bloqueado_20261126_193045.png
    """
    CARPETA_CAPTURAS.mkdir(exist_ok=True)
    # Los tests parametrizados tienen corchetes y espacios: se reemplazan por "_"
    nombre_limpio = re.sub(r"[^\w-]", "_", nombre_test).strip("_")
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = CARPETA_CAPTURAS / f"{nombre_limpio}_{fecha_hora}.png"
    driver.save_screenshot(str(ruta))
    return ruta