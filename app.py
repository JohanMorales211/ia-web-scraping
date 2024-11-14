import os
import json
import time
import logging
from flask import Flask, request, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

# Configuración de logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Cargar variables del archivo .env
load_dotenv()

# Obtener las variables de entorno
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
TWITTER_COOKIES_FILE = "cookies/twitter_cookies.json"

# Verifica si la API Key de Cerebras está cargada
if not CEREBRAS_API_KEY:
    logging.error("La variable de entorno CEREBRAS_API_KEY no está definida.")
    raise EnvironmentError("CEREBRAS_API_KEY no configurada en el archivo .env")

app = Flask(__name__)

def load_cookies(driver, filepath):
    """
    Carga las cookies almacenadas desde un archivo JSON en el navegador.
    """
    try:
        with open(filepath, "r") as f:
            cookies = json.load(f)
            for cookie in cookies:
                # Asegura de que el dominio de la cookie coincide con el dominio actual
                if 'domain' in cookie:
                    cookie['domain'] = '.x.com'
                driver.add_cookie(cookie)
        logging.debug(f"Cookies cargadas desde {filepath}")
    except Exception as e:
        logging.error(f"Error al cargar cookies desde {filepath}: {e}")

def init_driver_with_cookies():
    """
    Inicializa el navegador Firefox con las cookies cargadas para mantener la sesión.
    Siempre muestra la ventana del navegador (no headless).
    """
    try:
        options = Options()
        options.headless = False  # Siempre ejecutar con ventana visible
        logging.debug("Modo headless desactivado. Mostrando ventana del navegador.")

        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=options
        )
        driver.get("https://x.com")
        load_cookies(driver, TWITTER_COOKIES_FILE)
        driver.refresh()
        logging.debug("Navegador inicializado y cookies cargadas.")
        return driver
    except Exception as e:
        logging.error(f"Error al inicializar el driver con cookies: {e}")
        raise

def get_tweets(driver, topic, desired_count=10, max_scrolls=10):
    """
    Scrapea los últimos tweets relacionados con el tópico proporcionado hasta alcanzar desired_count.
    :param driver: Instancia del navegador Selenium.
    :param topic: Tópico para buscar tweets.
    :param desired_count: Número de tweets deseados.
    :param max_scrolls: Número máximo de desplazamientos para intentar.
    :return: Lista de tweets.
    """
    try:
        formatted_topic = topic.replace(' ', '+')
        search_url = f"https://x.com/search?q={formatted_topic}&src=typed_query"
        driver.get(search_url)
        logging.debug(f"Navegando a la URL de búsqueda: {search_url}")

        tweets = []
        scrolls = 0

        while len(tweets) < desired_count and scrolls < max_scrolls:
            time.sleep(3)  # Espera a que la página cargue los tweets
            tweet_elements = driver.find_elements(By.CSS_SELECTOR, 'article div[lang]')
            current_count = len(tweet_elements)
            tweets = [element.text for element in tweet_elements]
            logging.debug(f"Tweets encontrados tras el scroll {scrolls + 1}: {len(tweets)}")

            if len(tweets) >= desired_count:
                break

            # Desplaza hacia abajo para cargar más tweets
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            scrolls += 1

        # Retorna solo los primeros desired_count tweets
        tweets = tweets[:desired_count]
        logging.debug(f"Total de tweets obtenidos para el tema '{topic}': {len(tweets)}")
        return tweets
    except Exception as e:
        logging.error(f"Error al obtener tweets: {e}")
        return []

def analyze_tweets_summary_cerebras(tweets):
    if not tweets:
        logging.warning("No se proporcionaron tweets para analizar.")
        return "No se encontraron tweets para resumir."

    # Unir todos los tweets en un solo texto
    combined_text = "\n".join(tweets)
    logging.debug("Textos de tweets combinados para el resumen.")

    # Inicializar el cliente de Cerebras
    client = Cerebras(
        api_key=CEREBRAS_API_KEY
    )

    try:
        # Crea la solicitud de completions con un prompt orientado a generar un resumen cohesivo
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente que resume textos de Tweets en un tono neutral, generando un resumen cohesivo en párrafos que describa el contexto general."
                },
                {
                    "role": "user",
                    "content": f"Resume los siguientes tweets de manera clara y neutral, generando varios párrafos que describan el contexto general:\n{combined_text}"
                }
            ],
            model="llama3.1-8b",
            stream=False,
            max_completion_tokens=5000,
            temperature=0.2,
            top_p=1
        )

        # Registra la respuesta para inspección
        logging.debug(f"Respuesta de Cerebras: {response}")

        # Registra el tipo de respuesta
        logging.debug(f"Tipo de respuesta de Cerebras: {type(response)}")

        # Maneja la respuesta dependiendo de su estructura
        if isinstance(response, tuple):
            logging.debug("La respuesta es una tupla.")
            response = response[0]

        if hasattr(response, 'choices') and len(response.choices) > 0:
            # Accede a la primera elección
            choice = response.choices[0]

            # Accede al contenido del mensaje
            if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                summary = choice.message.content
                logging.debug(f"Resumen generado: {summary}")
                return summary.strip()
            else:
                logging.error("El primer elemento de 'choices' no tiene 'message.content'.")
                return "Error al generar el resumen."
        else:
            logging.error("La respuesta de la API no contiene 'choices' o está vacía.")
            return "Error al generar el resumen."

    except Exception as e:
        logging.error(f"Error al generar el resumen con Cerebras: {e}")
        return "Error al generar el resumen."

@app.route("/", methods=["GET"])
def index():
    """
    Ruta principal que renderiza el template index.html.
    """
    logging.debug("Cargando página principal.")
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Ruta que recibe un tópico, obtiene tweets relacionados y genera un resumen.
    Siempre muestra la ventana del navegador durante el scraping.
    """
    try:
        data = request.get_json()
        if not data:
            logging.warning("Solicitud POST sin cuerpo JSON.")
            return jsonify({"summary": "Solicitud inválida."}), 400

        topic = data.get("topic")

        logging.debug(f"Tópico recibido para análisis: {topic}")

        if not topic:
            logging.warning("No se proporcionó un tópico en la solicitud.")
            return jsonify({"summary": "No se proporcionó un tópico para analizar."}), 400

        driver = init_driver_with_cookies()
        tweets = get_tweets(driver, topic)
        driver.quit()
        logging.debug("Driver cerrado después de obtener tweets.")

        # Genera un resumen de todos los tweets usando Cerebras
        summary = analyze_tweets_summary_cerebras(tweets)
        logging.debug(f"Resumen generado para el tópico '{topic}': {summary}")

        # Devuelve tanto los tweets como el resumen
        return jsonify({"tweets": tweets, "summary": summary})

    except Exception as e:
        logging.error(f"Error en la ruta /analyze: {e}")
        return jsonify({"summary": "Error interno del servidor."}), 500

if __name__ == "__main__":
    # Ejecuta la aplicación Flask
    app.run(debug=True)