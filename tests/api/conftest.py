import pytest

from apis.jsonplaceholder_client import JsonPlaceholderClient


@pytest.fixture
def api():
    """Cliente de JSONPlaceholder nuevo para cada test; cierra la sesión al terminar."""
    cliente = JsonPlaceholderClient()
    yield cliente
    cliente.cerrar()