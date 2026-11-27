import os
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from configs.config import TIMEOUT

# Pausa (en segundos) antes de cada clic, para poder seguir la ejecución con la vista.
# Se configura con la variable de entorno PAUSA_VISUAL. Por defecto es 0 (rápido).
PAUSA_VISUAL = float(os.getenv("PAUSA_VISUAL", "0"))


def clic_con_espera(driver, localizador, pausa=PAUSA_VISUAL):
    elemento = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable(localizador))
    if pausa:
        time.sleep(pausa)
    elemento.click()