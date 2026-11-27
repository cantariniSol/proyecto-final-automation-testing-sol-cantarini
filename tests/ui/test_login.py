import pytest

from helpers.lector_datos import leer_json
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from configs.logger import obtener_logger

logger = obtener_logger(__name__)

DATOS_LOGIN = leer_json("login_data.json")


@pytest.mark.parametrize("datos", DATOS_LOGIN["usuarios_validos"], ids=lambda d: d["usuario"])
def test_login_exitoso(driver, datos):
    """Login válido: llega a /inventory.html, muestra 'Products' y el título 'Swag Labs'."""
    logger.info("Login válido con usuario '%s'", datos["usuario"])
    login = LoginPage(driver)
    login.abrir_login()
    login.ingresar(datos["usuario"], datos["password"])

    inventario = InventoryPage(driver)
    assert inventario.esta_en_inventario(), "No se llegó a Products en /inventory.html"
    assert driver.title == "Swag Labs", f"Título inesperado: {driver.title}"


@pytest.mark.parametrize("datos", DATOS_LOGIN["credenciales_invalidas"], ids=lambda d: d["caso"])
def test_login_invalido(driver, datos):
    """Caso negativo: con credenciales inválidas se muestra el error esperado y no se ingresa."""
    logger.info("Login inválido, caso '%s' (usuario: '%s')", datos["caso"], datos["usuario"])
    login = LoginPage(driver)
    login.abrir_login()
    login.ingresar(datos["usuario"], datos["password"])

    assert login.obtener_error() == datos["error"]
    assert "/inventory.html" not in driver.current_url, "No debería haber ingresado al inventario"