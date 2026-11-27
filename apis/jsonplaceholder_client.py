import logging

import requests

from configs.config import API_TIMEOUT, API_URL
from configs.logger import obtener_logger

logger = obtener_logger(__name__)


class JsonPlaceholderClient:
    """Cliente de la API JSONPlaceholder.

    Cumple el mismo rol que un Page Object en UI: los tests llaman a métodos con nombres
    de negocio (crear_post, obtener_usuario...) y no se ocupan de URLs ni de detalles HTTP.
    """

    def __init__(self, base_url=API_URL):
        self.base_url = base_url
        self.session = requests.Session()  # reutiliza la conexión entre peticiones

    def _enviar(self, metodo, endpoint, **kwargs):
        """Envía la petición HTTP y registra método, URL, cuerpo, código de estado y tiempo.

        Todas las llamadas pasan por acá, así quedan registradas en un único lugar.
        """
        url = f"{self.base_url}{endpoint}"
        detalle = f" | params: {kwargs['params']}" if kwargs.get("params") else ""
        detalle += f" | cuerpo: {kwargs['json']}" if "json" in kwargs else ""
        logger.info("%s %s%s", metodo, url, detalle)

        try:
            respuesta = self.session.request(metodo, url, timeout=API_TIMEOUT, **kwargs)
        except requests.RequestException as error:
            logger.error("Falló la conexión con %s: %s", url, error)
            raise

        milisegundos = respuesta.elapsed.total_seconds() * 1000
        nivel = logging.WARNING if respuesta.status_code >= 400 else logging.INFO
        logger.log(nivel, "Respuesta %s en %.0f ms", respuesta.status_code, milisegundos)
        return respuesta

    def cerrar(self):
        """Cierra la sesión HTTP."""
        self.session.close()

    # ---------- Posts ----------
    def listar_posts(self, user_id=None):
        """GET /posts (opcionalmente filtrado por usuario con ?userId=)."""
        params = {"userId": user_id} if user_id is not None else None
        return self._enviar("GET", "/posts", params=params)

    def obtener_post(self, post_id):
        """GET /posts/{id}"""
        return self._enviar("GET", f"/posts/{post_id}")

    def crear_post(self, datos):
        """POST /posts con el cuerpo en JSON."""
        return self._enviar("POST", "/posts", json=datos)

    def eliminar_post(self, post_id):
        """DELETE /posts/{id}"""
        return self._enviar("DELETE", f"/posts/{post_id}")

    # ---------- Usuarios y comentarios ----------
    def obtener_usuario(self, user_id):
        """GET /users/{id}"""
        return self._enviar("GET", f"/users/{user_id}")

    def listar_comentarios(self, post_id):
        """GET /posts/{id}/comments"""
        return self._enviar("GET", f"/posts/{post_id}/comments")