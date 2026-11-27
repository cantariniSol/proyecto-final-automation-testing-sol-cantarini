def validar_estructura(objeto, esquema):
    """Verifica que un objeto JSON tenga exactamente las claves del esquema y con el tipo esperado.

    esquema: dict {clave: tipo}, por ejemplo {"id": int, "title": str}
    """
    assert isinstance(objeto, dict), f"Se esperaba un objeto JSON y llegó {type(objeto).__name__}"
    assert set(objeto) == set(esquema), (
        f"Claves distintas. Esperadas: {sorted(esquema)} - Recibidas: {sorted(objeto)}"
    )
    for clave, tipo in esquema.items():
        assert isinstance(objeto[clave], tipo), (
            f"'{clave}' debería ser {tipo.__name__} y es {type(objeto[clave]).__name__}"
        )