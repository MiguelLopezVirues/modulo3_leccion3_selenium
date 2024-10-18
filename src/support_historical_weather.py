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

    city_names = randoms["city"]

    city_codes = get_city_code_plural(city_names)

    cities_df.loc[randoms.index,"code_wunder"] = pd.Series(city_codes)

    cities_df.to_csv("../data/cities_coordinates_codes.csv")

    return city_codes


def get_city_code_plural(city_names):

    code_list = list()

    driver = webdriver.Chrome()

    first_link = f"https://www.wunderground.com/"

    driver.get(first_link)

    handle_cookies(driver)

    for city_name in city_names:

        sleep(2)
        link = f"https://www.wunderground.com/weather/es/{city_name}"

        driver.get(link)

        city_code = get_city_code(driver)

        code_list.append(city_code)

    return code_list
        


def get_city_code(driver, url=None, city_name=None):

    #display table on the page
    sleep(3)
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

    driver.maximize_window()

    iframe = WebDriverWait(driver,15).until(EC.presence_of_element_located(('xpath','//*[@id="sp_message_iframe_1165301"]')))

    driver.switch_to.frame(iframe)
    try:
        driver.implicitly_wait(5)
        accept_button = driver.find_element("css selector","#notice > div.message-component.message-row.cta-buttons-container > div.message-component.message-column.cta-button-column.reject-column > button")
        accept_button.click()
    except:
        print("Cookies were not correctly handled or the pop up was not there.")
    
    driver.switch_to.default_content()

    
def get_city_table_df(city_code, year_number, month_number,driver=False):
    
    try:

        if int(month_number) < 1 and int(month_number) > 12:
            raise ValueError()
        
        elif int(year_number) < 2020 and int(year_number) > datetime.now().year:
            raise ValueError()
        
    except:
        print("You entered wrong values for year or month. Please enter numeric values. The first available year is 2020.")

    table_link = f"https://www.wunderground.com/dashboard/pws/{city_code}/table/{year_number}-{month_number}-01/{year_number}-{month_number}-31/monthly"
    print(table_link)

    try:
        if not driver:
            print("No driver")
            driver = webdriver.Chrome()
            driver.get(table_link)
            driver.maximize_window()
            handle_cookies(driver)

        else:
            print("Reusing driver")
            driver.get(table_link)

    except:
        print("The city entered was not found.")


    return scrape_table(driver, city_code) , driver

def scrape_table(driver, city_code):
    # get element with the table rows inside
    try:
        driver.implicitly_wait(10)
        rows = driver.find_element("css selector", "#main-page-content > div > div > div > lib-history > div.history-tabs > lib-history-table > div > div").text.split("\n")

    except:
        print("There has been a problem getting the element.")
    
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

    print(df_table)
    
    return df_table
    

def multi_scrape_table(n_cities, cities_df, n_months=1, start_year=2024, start_month=1):

    city_codes = random_cities(n_cities, cities_df)

    df_final = pd.DataFrame()

    driver = None

    for month in range(start_month, start_month + n_months):
        for city_code in city_codes:

            try:
                df, driver = get_city_table_df(city_code,start_year,month, driver)
                df_final = pd.concat([df_final,df],axis=0)

            except:
                print(f"There was a problem scraping the citiy code {city_code} for the month {month}.")
        
            df_final.to_csv("../data/historical_weather_saved.csv")
    
    driver.close()
    return df_final
        

