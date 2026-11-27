import base64

import pytest
from pytest_html import extras as html_extras
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from configs.config import URL, USUARIO
from configs.logger import obtener_logger
from helpers.capturas import guardar_captura

logger = obtener_logger(__name__)


@pytest.fixture
def driver():
    """Abre un Chrome nuevo para cada test y lo cierra al terminar."""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def driver_logueado(driver):
    """Driver con la sesión de standard_user ya iniciada (por cookie, sin pasar por el login)."""
    driver.get(URL)
    driver.add_cookie({"name": "session-username", "value": USUARIO})
    driver.get(URL + "inventory.html")
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si un test de UI falla, guarda una captura y la adjunta al reporte HTML."""
    resultado = yield
    reporte = resultado.get_result()

    # Solo interesan los fallos en la preparación (setup) o en el test en sí (call)
    if reporte.when not in ("setup", "call") or not reporte.failed:
        return

    # Los tests de API no usan navegador; tampoco hay captura si Chrome no llegó a abrirse
    driver = item.funcargs.get("driver")
    if driver is None:
        return

    try:
        ruta = guardar_captura(driver, item.name)
    except Exception as error:  # por ejemplo, si el navegador se cerró inesperadamente
        logger.warning("No se pudo guardar la captura de %s: %s", item.name, error)
        return

    logger.error("Falló %s - captura guardada en %s", item.name, ruta)

    # Se adjunta en base64 para que la imagen quede dentro del HTML (reporte autocontenido)
    imagen_base64 = base64.b64encode(ruta.read_bytes()).decode("utf-8")
    extras = getattr(reporte, "extras", [])
    extras.append(html_extras.png(imagen_base64, name=ruta.name))
    reporte.extras = extras


def pytest_html_report_title(report):
    """Título del reporte HTML."""
    report.title = "Reporte de pruebas - Automation Testing"