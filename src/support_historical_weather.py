# Importamos las librerías que necesitamos

# Librerías de extracción de datos
# -----------------------------------------------------------------------

# Importaciones:
# Beautifulsoup
from bs4 import BeautifulSoup

# Requests
import requests

import pandas as pd
import numpy as np

from time import sleep

# Importar librerías para automatización de navegadores web con Selenium
# -----------------------------------------------------------------------
from selenium import webdriver  # Selenium es una herramienta para automatizar la interacción con navegadores web.
from webdriver_manager.chrome import ChromeDriverManager  # ChromeDriverManager gestiona la instalación del controlador de Chrome.
from selenium.webdriver.common.keys import Keys  # Keys es útil para simular eventos de teclado en Selenium.
from selenium.webdriver.support.ui import Select  # Select se utiliza para interactuar con elementos <select> en páginas web.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException # Excepciones comunes de selenium que nos podemos encontrar 

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my-geopy-app")
import random
import re
import datetime

def random_cities(n_cities, cities_df):

    randoms = cities_df.sample(n=n_cities)
    code_list = list()
    for idx,random_city in randoms.iterrows():
        if random_city["code_wunder"] == "":
            random_city["code_wunder"] = get_city_code(random_city["city"])
            cities_df.loc[cities_df["city"] == random_city["city"] ,"code_wunder"] = random_city["code_wunder"]

        code_list.append(random_city["code_wunder"])
    
    return code_list

 
        
def get_city_code(city_name):
    link = f"https://www.wunderground.com/weather/es/{city_name}"

    driver = webdriver.Chrome()
    driver.get(link)

    driver.maximize_window()

    handle_cookies(driver)

    #display table on the page
    sleep(5)
    try:
        code_link = driver.find_element("css selector","#inner-content > div.region-content-top > lib-city-header > div:nth-child(1) > div > div > a.station-name").get_attribute("href")
        driver.get(code_link)
    except:
        print("Url to capture the city_code not well got.")
        
    sleep(3)
    code = driver.find_element("css selector", "#inner-content > div.region-content-top > app-dashboard-header > div.dashboard__header.small-12.ng-star-inserted > div > div.heading > h1")
    code = code.text.split(" - ")[-1]
    return code

def handle_cookies(driver):
    iframe = WebDriverWait(driver,15).until(EC.presence_of_element_located(('xpath','//*[@id="sp_message_iframe_1165301"]')))
    driver.switch_to.frame(iframe)
    try:
        driver.implicitly_wait(5)
        accept_button = driver.find_element("css selector","#notice > div.message-component.message-row.cta-buttons-container > div.message-component.message-column.cta-button-column.reject-column > button")
        accept_button.click()
    except:
        print("Cookies were not correctly handled.")
    
    driver.switch_to.default_content()

    
def get_city_table(city_code, year_number, month_number):
    try:
        if int(month_number) < 1 and int(month_number) > 12:
            raise ValueError()
        elif int(year_number) < 2020 and int(year_number) > datetime.now().year:
            raise ValueError()
    except:
        print("You entered wrong values for year or month. Please enter numeric values. The first available year is 2020.")

    table_link = f"https://www.wunderground.com/dashboard/pws/{city_code}/table/{year_number}-{month_number}-01/{year_number}-{month_number}-31/monthly"

    try:
        driver = webdriver.Chrome()
        driver.get(table_link)
    except:
        print("The city entered was not found.")

    driver.maximize_window()

    handle_cookies(driver)
    
    driver.execute_script('window.scrollBy(0, 2000)')

    sleep(4)

    return scrape_table(driver, city_code)

def scrape_table(driver, city_code):
    # get element with the table rows inside
    rows = driver.find_element("css selector", "#main-page-content > div > div > div > lib-history > div.history-tabs > lib-history-table > div > div").text.split("\n")

    # remove special characters and split into cells
    df_table = pd.Series([row.replace("°F","").replace("%","").replace("mph","").replace("in","") for row in rows])
    df_table = df_table.str.split(expand=True)

    # format columns
    df_table.columns = df_table.iloc[1]
    df_table = df_table[2:]
    df_table["Date"] = pd.to_datetime(df_table["Date"])
    df_table.columns = ['Date', 'Temp High ºF', 'Temp Avg ºF', 'Temp Low ºF', 'Dew High ºF', 'Dew Avg ºF', 'Dew Low ºF', 'Humid High %', 'Humid Avg %',
        'Humid Low %', 'Speed High mph', 'Speed Avg mph', 'Speed Low mph', 'Pressure High in', 'Pressure Low in', 'Precip Sum in']
    
    # add city code
    df_table["city_code"] = city_code
    
    return df_table
    


