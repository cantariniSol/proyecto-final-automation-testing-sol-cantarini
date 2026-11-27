import os

URL = "https://www.saucedemo.com/"
USUARIO = "standard_user"
PASSWORD = "secret_sauce"
TIMEOUT = 10

# Chrome sin ventana (para CI). Se activa con la variable de entorno HEADLESS=true
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# --- API ---
API_URL = "https://jsonplaceholder.typicode.com"
API_TIMEOUT = 10            # segundos máximos de espera por respuesta
API_TIEMPO_MAXIMO = 3       # segundos aceptables para considerar la respuesta "rápida"