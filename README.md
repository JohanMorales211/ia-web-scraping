# Análisis de Tweets en Tiempo Real con IA 🐦🧠

**Explora el poder del web scraping y el procesamiento del lenguaje natural para analizar las tendencias en Twitter/X en tiempo real, con visualizaciones interactivas y resúmenes generados por IA.**

Este proyecto utiliza técnicas de web scraping para recopilar tweets de Twitter/X en tiempo real, los analiza utilizando inteligencia artificial para identificar tendencias y sentimientos, y presenta los resultados de manera visual e interactiva.

![Interfaz de análisis](https://img.freepik.com/fotos-premium/estamos-buscando-crear-imagen-realista-letra-x-efectos-luz-sombras-representar_693504-2031.jpg)

## Características Principales ✨

*   **Recolección de Tweets en Tiempo Real:**  Captura tweets basados en búsquedas específicas o hashtags.
*   **Análisis de Sentimiento:**  Determina el sentimiento general (positivo, negativo, neutral) expresado en los tweets.
*   **Identificación de Tendencias:**  Detecta temas y palabras clave emergentes dentro de los tweets recopilados.
*   **Resúmenes Generados por IA:**  Obtén resúmenes concisos y comprensibles de las tendencias identificadas.
*   **Visualizaciones Interactivas:**  Explora gráficos y tablas dinámicas para comprender mejor los datos.
*   **Configuración Sencilla:**  Fácil de configurar con variables de entorno.

## Comenzando 🚀

Sigue estos pasos para poner en marcha la aplicación:

### Configuración Inicial ⚙️

1. **Crea el archivo `.env`:** En la raíz del proyecto, crea un archivo llamado `.env`. Este archivo contendrá tus credenciales e información de configuración.

2. **Define las variables de entorno:** Abre el archivo `.env` con un editor de texto y añade las siguientes variables, reemplazando los valores de ejemplo con tu propia información:

    ```ini
    # Credenciales de Twitter/X
    X_USERNAME="tu_usuario_de_twitter"
    X_PASSWORD="tu_contraseña_de_twitter"

    # API Key de Cerebras (obténla en https://www.cerebras.net/cloud/)
    CEREBRAS_API_KEY="tu_clave_api"

    # Configuración opcional de scraping
    MAX_TWEETS=15  # Número máximo de tweets a recolectar por búsqueda
    SCROLL_TIMEOUT=5  # Tiempo de espera entre scrolls al cargar más tweets (segundos)
    ```

    **Importante:** Mantén este archivo seguro y no lo compartas públicamente.

### Instalación Completa 🛠️

1. **Clona el repositorio:**

    ```bash
    git clone https://github.com/JohanMorales211/ia-web-scraping.git
    ```

2. **Navega al directorio del proyecto:**

    ```bash
    cd ia-web-scraping
    ```

3. **Configura el entorno virtual (recomendado):**

    ```bash
    # Crea el entorno virtual
    python -m venv venv
    # Activa el entorno virtual
    # En Windows
    venv\Scripts\activate
    # En Linux/Mac
    source venv/bin/activate
    ```

    Usar un entorno virtual ayuda a aislar las dependencias de este proyecto.

4. **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

    Este comando instalará todas las bibliotecas necesarias listadas en el archivo `requirements.txt`.

5. **Genera las cookies de sesión de Twitter/X (primera ejecución):**

    ```bash
    python twitter_scraper.py
    ```

    Este script abrirá automáticamente un navegador donde deberás iniciar sesión en tu cuenta de Twitter/X. Esto generará las cookies necesarias para realizar el scraping. **Asegúrate de cerrar el navegador una vez que la sesión se haya guardado.**

6. **Inicia la aplicación:**

    ```bash
    python app.py
    ```

    Este comando ejecutará el servidor de la aplicación.

7. **Accede a la aplicación en tu navegador:**

    Abre tu navegador web y ve a la siguiente dirección:

    ```
    http://localhost:5000
    ```

    ¡Deberías ver la interfaz de la aplicación!

## Obtención de Credenciales Clave 🔑

*   **Twitter/X:**
    *   Necesitas una cuenta de Twitter/X activa.
    *   Las credenciales (usuario y contraseña) se utilizan para la autenticación inicial y la generación de cookies de sesión para el scraping.
    *   Considera utilizar una cuenta secundaria para fines de scraping para mayor seguridad.

*   **Cerebras:**
    *   Regístrate en la plataforma Cerebras Cloud (https://cloud.cerebras.ai/) para obtener una API Key.
    *   Esta API Key es necesaria para utilizar los servicios de procesamiento de lenguaje natural y generación de resúmenes basados en IA.
    *   Busca en la documentación de Cerebras cómo obtener tu API Key.

## Estructura del Archivo `.env` Ejemplo ✅

Asegúrate de que tu archivo `.env` tenga la siguiente estructura, reemplazando los valores de ejemplo con tus datos reales. **Evita incluir comentarios en el archivo `.env` en un entorno de producción.**

```ini
X_USERNAME="johantwitter"
X_PASSWORD="miclaveSegura123"
CEREBRAS_API_KEY="cs-abc123...xyz"
MAX_TWEETS=20
SCROLL_TIMEOUT=3
