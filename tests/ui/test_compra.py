import pytest

from helpers.lector_datos import leer_csv
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage
from configs.logger import obtener_logger

logger = obtener_logger(__name__)

DATOS_COMPRA = leer_csv("checkout_data.csv")


@pytest.mark.parametrize("datos", DATOS_COMPRA, ids=lambda d: d["producto"])
def test_compra_completa(driver_logueado, datos):
    """Flujo completo: detalle del producto, carrito, checkout y confirmación de la compra."""
    nombre_producto = datos["producto"]
    logger.info("Compra de '%s' para %s %s", nombre_producto, datos["nombre"], datos["apellido"])

    inventario = InventoryPage(driver_logueado)
    producto = ProductPage(driver_logueado)
    carrito = CartPage(driver_logueado)
    checkout = CheckoutPage(driver_logueado)

    inventario.abrir_detalle(nombre_producto)
    assert producto.nombre() == nombre_producto
    producto.agregar()
    assert inventario.esperar_cantidad(1)

    inventario.abrir_carrito()
    assert carrito.nombres_productos() == [nombre_producto]

    logger.info("Producto en el carrito; se completa el checkout")
    carrito.ir_a_checkout()
    checkout.completar_datos(datos["nombre"], datos["apellido"], datos["codigo_postal"])
    assert checkout.producto_en_resumen() == nombre_producto

    logger.info("Finalizar la compra y verificar la confirmación")
    checkout.finalizar()
    assert checkout.mensaje_final() == "Thank you for your order!"