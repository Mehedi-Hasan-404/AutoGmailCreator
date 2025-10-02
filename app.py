import time
import csv
import random
import string
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver as wire_webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
import geckodriver_autoinstaller

# Configuration
AUTO_GENERATE_USERINFO = True
SOCKS_PROXY = None
HEADLESS = True
USE_FIREFOX = False

# User-Agent and Proxy setup
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
seleniumwire_options = {
    'request_storage_base_dir': '/tmp/seleniumwire',
    'disable_encoding': True,
    'proxy': {
        'http': SOCKS_PROXY,
        'https': SOCKS_PROXY,
    }
}

# Browser setup
options = Options()
options.add_argument(f"user-agent={user_agent}")
if HEADLESS:
    options.add_argument('--headless')
if USE_FIREFOX:
    geckodriver_autoinstaller.install()
    options = FirefoxOptions()
    options.add_argument("-headless")
    driver = wire_webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options, seleniumwire_options=seleniumwire_options)
else:
    options.add_argument("--start-maximized")
    driver = wire_webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options, seleniumwire_options=seleniumwire_options)

# Function to generate random username
def generate_username(first_name, last_name):
    return f"{first_name.lower()}.{last_name.lower()}{random.randint(1000, 9999)}"

# Function to create Gmail account
def create_account(first_name, last_name, birth_day, birth_month, birth_year, gender, password):
    driver.get("https://accounts.google.com/signup")
    time.sleep(2)

    driver.find_element(By.ID, "firstName").send_keys(first_name)
    driver.find_element(By.ID, "lastName").send_keys(last_name)
    username = generate_username(first_name, last_name)
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.NAME, "Passwd").send_keys(password)
    driver.find_element(By.NAME, "ConfirmPasswd").send_keys(password)
    driver.find_element(By.XPATH, "//span[text()='Next']").click()
    time.sleep(2)

    driver.find_element(By.ID, "phoneNumberId").send_keys("YOUR_PHONE_NUMBER")
    driver.find_element(By.XPATH, "//span[text()='Next']").click()
    time.sleep(2)

    driver.find_element(By.ID, "day").send_keys(birth_day)
    driver.find_element(By.ID, "month").send_keys(birth_month)
    driver.find_element(By.ID, "year").send_keys(birth_year)
    driver.find_element(By.XPATH, "//span[text()='Next']").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "//span[text()='Next']").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "//span[text()='I agree']").click()
    time.sleep(2)

    print(f"Account created for {first_name} {last_name} ({username}@gmail.com)")

# Read user data from CSV
with open('user.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        first_name = row['first_name']
        last_name = row['last_name']
        birth_day = row['birth_day']
        birth_month = row['birth_month']
        birth_year = row['birth_year']
        gender = row['gender']
        password = row['password']
        create_account(first_name, last_name, birth_day, birth_month, birth_year, gender, password)

driver.quit()
