import pytest

from apis.esquemas import ESQUEMA_POST
from configs.config import API_TIEMPO_MAXIMO
from helpers.lector_datos import leer_json
from helpers.validaciones_api import validar_estructura

POSTS_A_CREAR = leer_json("posts_data.json")


def test_obtener_post_existente(api):
    """GET /posts/1: código 200, JSON con la estructura de un post, contenido y tiempo de respuesta."""
    respuesta = api.obtener_post(1)

    # 1. Código HTTP
    assert respuesta.status_code == 200
    assert "application/json" in respuesta.headers["Content-Type"]

    # 2. Estructura
    post = respuesta.json()
    validar_estructura(post, ESQUEMA_POST)

    # 3. Contenido
    assert post["id"] == 1
    assert post["userId"] == 1
    assert post["title"].strip() != "", "El título no debería estar vacío"

    # 4. Tiempo de respuesta
    segundos = respuesta.elapsed.total_seconds()
    assert segundos < API_TIEMPO_MAXIMO, f"Respuesta lenta: {segundos:.2f}s"


def test_listar_posts(api):
    """GET /posts: devuelve una lista de 100 posts y todos tienen la estructura esperada."""
    respuesta = api.listar_posts()

    assert respuesta.status_code == 200
    posts = respuesta.json()
    assert isinstance(posts, list)
    assert len(posts) == 100
    for post in posts:
        validar_estructura(post, ESQUEMA_POST)


@pytest.mark.parametrize("datos", POSTS_A_CREAR, ids=lambda d: d["title"])
def test_crear_post(api, datos):
    """POST /posts: código 201 y la respuesta devuelve los datos enviados más un id nuevo."""
    respuesta = api.crear_post(datos)

    assert respuesta.status_code == 201
    creado = respuesta.json()
    validar_estructura(creado, ESQUEMA_POST)

    for clave, valor in datos.items():
        assert creado[clave] == valor, f"'{clave}' no coincide con lo enviado"
    assert creado["id"] == 101, "JSONPlaceholder asigna siempre el id 101 a un post nuevo"