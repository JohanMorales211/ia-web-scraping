import os
import time
import json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Carga las variables del archivo .env
load_dotenv()
X_USERNAME = os.getenv("X_USERNAME")
X_PASSWORD = os.getenv("X_PASSWORD")

COOKIES_FOLDER = "cookies"
os.makedirs(COOKIES_FOLDER, exist_ok=True)
COOKIES_FILE = os.path.join(COOKIES_FOLDER, "twitter_cookies.json")

def init_driver():
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    return driver

def save_cookies(driver, filepath):
    with open(filepath, "w") as f:
        json.dump(driver.get_cookies(), f)

def login_to_twitter(driver):
    driver.get("https://x.com/i/flow/login")
    time.sleep(5)
    driver.find_element(By.NAME, "text").send_keys(X_USERNAME + Keys.RETURN)
    time.sleep(3)
    driver.find_element(By.NAME, "password").send_keys(X_PASSWORD + Keys.RETURN)
    time.sleep(5)

if __name__ == "__main__":
    driver = init_driver()
    login_to_twitter(driver)
    save_cookies(driver, COOKIES_FILE)
    driver.quit()
    print("[INFO] Cookies guardadas exitosamente.")
