"""Estructura esperada de cada recurso de JSONPlaceholder: {clave: tipo}."""

ESQUEMA_POST = {"userId": int, "id": int, "title": str, "body": str}

ESQUEMA_USUARIO = {
    "id": int,
    "name": str,
    "username": str,
    "email": str,
    "address": dict,
    "phone": str,
    "website": str,
    "company": dict,
}

ESQUEMA_COMENTARIO = {"postId": int, "id": int, "name": str, "email": str, "body": str}