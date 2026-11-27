from apis.esquemas import ESQUEMA_COMENTARIO, ESQUEMA_POST, ESQUEMA_USUARIO
from helpers.validaciones_api import validar_estructura

ID_USUARIO = 1


def test_flujo_usuario_posts_comentarios(api):
    """Encadenamiento: cada petición usa un dato obtenido de la respuesta anterior.

    1. GET /users/1                 -> se obtiene el id del usuario
    2. GET /posts?userId=<id>       -> se obtienen sus posts y se toma el primero
    3. GET /posts/<id>/comments     -> se obtienen los comentarios de ese post
    """
    # 1. Usuario
    respuesta_usuario = api.obtener_usuario(ID_USUARIO)
    assert respuesta_usuario.status_code == 200
    usuario = respuesta_usuario.json()
    validar_estructura(usuario, ESQUEMA_USUARIO)
    assert "@" in usuario["email"]

    # 2. Posts del usuario (depende del id obtenido en el paso 1)
    respuesta_posts = api.listar_posts(user_id=usuario["id"])
    assert respuesta_posts.status_code == 200
    posts = respuesta_posts.json()
    assert len(posts) > 0, f"El usuario {usuario['username']} no tiene posts"
    for post in posts:
        validar_estructura(post, ESQUEMA_POST)
        assert post["userId"] == usuario["id"], "Llegó un post de otro usuario"

    # 3. Comentarios del primer post (depende del id obtenido en el paso 2)
    primer_post = posts[0]
    respuesta_comentarios = api.listar_comentarios(primer_post["id"])
    assert respuesta_comentarios.status_code == 200
    comentarios = respuesta_comentarios.json()
    assert len(comentarios) > 0
    for comentario in comentarios:
        validar_estructura(comentario, ESQUEMA_COMENTARIO)
        assert comentario["postId"] == primer_post["id"], "Llegó un comentario de otro post"