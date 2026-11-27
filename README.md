# Proyecto Final – Automation Testing

[![Tests automatizados](https://github.com/cantariniSol/proyecto-final-automation-testing-sol-cantarini/actions/workflows/tests.yml/badge.svg)](https://github.com/cantariniSol/proyecto-final-automation-testing-sol-cantarini/actions/workflows/tests.yml)

Framework de automatización de pruebas en **Python** que combina:

- **Pruebas de UI** sobre [saucedemo.com](https://www.saucedemo.com/) con Selenium WebDriver y el patrón **Page Object Model**.
- **Pruebas de API** sobre [JSONPlaceholder](https://jsonplaceholder.typicode.com/) con la biblioteca Requests.

Incluye datos de prueba en archivos externos (JSON y CSV), capturas de pantalla automáticas cuando un test falla, reportes HTML, logging detallado e integración continua con GitHub Actions.

> Trabajo Final Integrador del curso de Automation Testing.

---

## Propósito

Demostrar un framework de testing automatizado **mantenible y escalable**:

- La lógica de los tests está separada de la interacción con la página (Page Objects) y con la API (cliente HTTP).
- Los datos de prueba viven fuera del código, así se agregan casos sin tocar los tests.
- Cada test es independiente: abre su propio navegador o cliente, así la falla de uno no afecta a los demás.
- Cada ejecución deja evidencia clara: reporte HTML, log y capturas de los fallos.

---

## Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje principal |
| Pytest | Framework de testing: fixtures, parametrización, hooks |
| Selenium WebDriver | Automatización del navegador (Google Chrome) |
| webdriver-manager | Descarga automática del ChromeDriver compatible |
| Requests | Pruebas de API REST |
| pytest-html | Reporte HTML con resultados, duración, logs y capturas |
| logging (estándar de Python) | Registro de pasos de ejecución |
| GitHub Actions | Integración continua: ejecuta los tests en cada push |
| Git y GitHub | Control de versiones, con una rama por funcionalidad |

---

## Estructura del proyecto

```
├── .github/workflows/tests.yml   # Pipeline de CI (GitHub Actions)
├── apis/                         # Capa de API
│   ├── jsonplaceholder_client.py #   Cliente HTTP: un método por endpoint, con logging
│   └── esquemas.py               #   Estructura esperada (claves y tipos) de cada recurso
├── configs/
│   ├── config.py                 # URLs, usuario, timeouts, modo headless
│   └── logger.py                 # Obtención de loggers
├── data/                         # Datos de prueba externos
│   ├── login_data.json           #   Usuarios válidos y credenciales inválidas
│   ├── checkout_data.csv         #   Productos y datos de compra
│   └── posts_data.json           #   Posts a crear en la API
├── helpers/
│   ├── esperas.py                # Clic con espera explícita
│   ├── lector_datos.py           # Lectura de JSON y CSV
│   ├── capturas.py               # Capturas con nombre de test y fecha/hora
│   └── validaciones_api.py       # Validación de estructura de respuestas JSON
├── pages/                        # Page Objects (UI)
│   ├── base_page.py              #   Acciones comunes: abrir, clic, escribir, esperar
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── conftest.py               # Fixtures del navegador, captura ante fallos, logs por test
│   ├── ui/                       # Tests de UI
│   └── api/                      # Tests de API (con su fixture "api")
├── reports/                      # Reporte HTML (se genera al ejecutar)
├── screenshots/                  # Capturas de tests fallidos (se generan al ejecutar)
├── logs/                         # Log de la ejecución (se genera al ejecutar)
├── pytest.ini                    # Configuración de pytest (reporte, logging)
└── requirements.txt              # Dependencias
```

---

## Casos de prueba

### UI – saucedemo.com (12 ejecuciones)

| Test | Qué valida | Datos |
|---|---|---|
| `test_login_exitoso` | Login válido: llega a `/inventory.html`, título "Products" y "Swag Labs" | `login_data.json` (3 usuarios) |
| `test_login_invalido` | **Caso negativo:** contraseña incorrecta, usuario bloqueado, usuario vacío y contraseña vacía muestran el error correcto | `login_data.json` (4 casos) |
| `test_catalogo` | Catálogo, datos del primer producto, detalle, agregar y quitar | — |
| `test_carrito` | Agregar, quitar, cancelar el checkout y verificar el contador y el contenido del carrito | — |
| `test_compra_completa` | Flujo completo: detalle → carrito → checkout → "Thank you for your order!" | `checkout_data.csv` (3 compras) |

### API – JSONPlaceholder (7 ejecuciones)

| Test | Método | Qué valida |
|---|---|---|
| `test_obtener_post_existente` | GET | Código 200, `Content-Type`, estructura, contenido y tiempo de respuesta |
| `test_listar_posts` | GET | 100 posts, todos con la estructura esperada |
| `test_crear_post` | POST | Código 201, devuelve los datos enviados y un `id` nuevo (parametrizado con `posts_data.json`) |
| `test_eliminar_post` | DELETE | Código 200 y cuerpo vacío |
| `test_obtener_post_inexistente_devuelve_404` | GET | **Caso de error:** código 404 |
| `test_flujo_usuario_posts_comentarios` | GET ×3 | **Peticiones encadenadas:** usuario → sus posts → comentarios del primer post |

> JSONPlaceholder es una API de práctica que no guarda los cambios: el POST responde con el recurso creado pero no lo persiste. Por eso el flujo encadenado usa datos existentes.

---

## Instalación

**Requisitos:** Python 3.10 o superior (el proyecto usa 3.12), Google Chrome y Git.

```bash
# 1. Clonar el repositorio
git clone https://github.com/cantariniSol/proyecto-final-automation-testing-sol-cantarini.git
cd proyecto-final-automation-testing-sol-cantarini

# 2. Crear y activar un entorno virtual
python3 -m venv venv
source venv/bin/activate          # Linux / macOS
# source venv/Scripts/activate    # Windows (Git Bash)
# venv\Scripts\Activate.ps1       # Windows (PowerShell)

# 3. Instalar las dependencias
pip install -r requirements.txt
```

El ChromeDriver se descarga solo (webdriver-manager), según la versión de Chrome instalada.

---

## Ejecución

| Comando | Qué ejecuta |
|---|---|
| `pytest` | Todos los tests (UI + API) y genera el reporte HTML |
| `pytest tests/ui` | Solo los tests de UI |
| `pytest tests/api` | Solo los tests de API (rápidos, no abren el navegador) |
| `pytest -k login` | Solo los tests cuyo nombre contiene "login" |
| `HEADLESS=true pytest` | Chrome sin ventana (así corre en CI) |
| `PAUSA_VISUAL=2 pytest tests/ui` | Pausa de 2 s antes de cada clic, para seguir la ejecución con la vista |
| `pytest -o log_cli=true` | Muestra los logs en vivo en la terminal |

En PowerShell las variables de entorno se definen así: `$env:HEADLESS="true"; pytest`.

---

## Reportes y evidencias

Cada ejecución genera tres tipos de evidencia (no se versionan en git):

### 1. Reporte HTML – `reports/reporte.html`

Archivo autocontenido (estilos e imágenes adentro); se abre con cualquier navegador.

- **Encabezado:** fecha, duración total y resumen con la cantidad de tests en cada estado (*Passed*, *Failed*, *Skipped*, *Error*...). Cada estado es un filtro: se puede tildar o destildar para ver solo los fallidos, por ejemplo.
- **Tabla de resultados:** una fila por test con su **resultado**, su **nombre** y su **duración**. Los tests parametrizados muestran el caso entre corchetes, por ejemplo `test_login_invalido[usuario_bloqueado]`.
- **Detalle (clic en la fila):**
  - el error y la línea del `assert` que falló;
  - la sección *Captured log*, con los pasos que registró ese test;
  - en los tests de UI fallidos, **la captura de pantalla** del momento del fallo.

Cómo interpretarlo: un test *Failed* significa que un `assert` no se cumplió (diferencia entre lo esperado y lo obtenido). Un test *Error* significa que falló la preparación, por ejemplo que no se pudo abrir el navegador.

### 2. Capturas – `screenshots/`

Se generan **solo cuando falla un test de UI**, con el nombre del test y la fecha/hora:

```
screenshots/test_compra_completa_Sauce_Labs_Backpack_20261126_193045.png
```

### 3. Log – `logs/ejecucion.log`

Se reescribe en cada ejecución. Formato: `fecha hora [NIVEL] módulo: mensaje`.

- Cada test empieza con `INICIO` y termina con `FIN`, junto con su resultado y su duración.
- Los tests de UI registran sus pasos y cada acción (clic, escritura, espera de URL).
- El cliente de API registra método, URL, cuerpo enviado, código de respuesta y tiempo en ms.
- Niveles: `INFO` (normal), `WARNING` (respuesta 4xx/5xx de la API) y `ERROR` (test fallido o captura guardada).

Las contraseñas no se registran nunca.

```bash
grep -E "ERROR|WARNING" logs/ejecucion.log   # ir directo a los problemas
grep -E "INICIO|FIN" logs/ejecucion.log      # resumen test por test
```

---

## Datos de prueba

Los datos están en `data/` y se cargan con `helpers/lector_datos.py`. Los tests usan `@pytest.mark.parametrize`, así que **agregar un caso es agregar un elemento al archivo**, sin tocar el código:

- `login_data.json`: un nuevo objeto en `credenciales_invalidas` (con `caso`, `usuario`, `password` y `error`) crea un nuevo test negativo.
- `checkout_data.csv`: una nueva fila crea una nueva compra completa.
- `posts_data.json`: un nuevo objeto crea un nuevo test de POST.

---

## Integración continua (GitHub Actions)

El workflow `.github/workflows/tests.yml` se ejecuta **en cada push** (a cualquier rama), en los pull requests a `main` y a mano desde la pestaña *Actions*:

1. Prepara una máquina Ubuntu con Python 3.12 y Google Chrome.
2. Instala las dependencias de `requirements.txt`.
3. Ejecuta `pytest` en modo headless.
4. Sube **siempre**, aunque haya fallos, el reporte, el log y las capturas como artefacto `resultados-tests-<n>`.

Para ver los resultados: pestaña **Actions** → elegir la ejecución → en **Artifacts**, descargar el `.zip` y abrir `reports/reporte.html`.

---

## Cómo agregar nuevas pruebas

**UI**
1. Si la página es nueva, crear su Page Object en `pages/` heredando de `BasePage`, con sus localizadores como constantes y un método por acción.
2. Crear el test en `tests/ui/test_<funcionalidad>.py` usando la fixture `driver` (navegador limpio) o `driver_logueado` (sesión iniciada).
3. Si usa datos, agregarlos en `data/` y parametrizar con `leer_json` o `leer_csv`.

La captura ante fallos, el log de inicio y fin y el reporte se aplican solos.

**API**
1. Agregar el método del endpoint en `apis/jsonplaceholder_client.py` (y su esquema en `apis/esquemas.py`).
2. Crear el test en `tests/api/` usando la fixture `api`.

---

## Buenas prácticas aplicadas

- **Page Object Model:** los tests no contienen localizadores ni llamadas directas a Selenium.
- **Esperas explícitas** (`WebDriverWait`) en lugar de pausas fijas.
- **Tests independientes:** cada test usa su propio navegador o sesión HTTP.
- **Data-driven testing** con archivos JSON y CSV.
- **Sin credenciales sensibles** en el código ni en los logs.
- **Una rama por funcionalidad**, fusionada a `main` con `--no-ff` para conservar el historial.

---

## Autora

**Sol Cantarini**