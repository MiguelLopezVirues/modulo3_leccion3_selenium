from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from selenium.webdriver.chrome.options import Options

from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from selenium.webdriver.chrome.options import Options

def handle_cookies(driver):
    driver.maximize_window()
    iframe = WebDriverWait(driver, 15).until(EC.presence_of_element_located(('xpath', '//*[@id="sp_message_iframe_1165301"]')))
    driver.switch_to.frame(iframe)
    try:
        accept_button = driver.find_element("css selector", "#notice > div.message-component.message-row.cta-buttons-container > div.message-component.message-column.cta-button-column.reject-column > button")
        accept_button.click()
    except:
        print("Cookies were not correctly handled or the pop-up was not there.")
    driver.switch_to.default_content()

def scrape_city_code(city_name):
    driver = webdriver.Chrome()
    driver.maximize_window() 
    link = f"https://www.wunderground.com/weather/es/{city_name}"
    driver.get(link)
    handle_cookies(driver)
    city_code = get_city_code(driver)
    driver.quit()
    return city_code

def get_city_code(driver):
    sleep(2)
    try:
        code_link = driver.find_element("css selector", "#inner-content > div.region-content-top > lib-city-header > div:nth-child(1) > div > div > a.station-name").get_attribute("href")
        driver.get(code_link)
    except:
        print("Error to capture the city code link.")
    
    sleep(1)
    code = driver.find_element("css selector", "#inner-content > div.region-content-top > app-dashboard-header > div.dashboard__header.small-12.ng-star-inserted > div > div.heading > h1")
    code = code.text.split(" - ")[-1]
    return code

def get_city_table_df(city_code, year_number, month_number, driver=None):
    try:
        if not (1 <= int(month_number) <= 12) or not (2024 <= int(year_number) <= datetime.datetime.now().year):
            raise ValueError("Invalid month or year.")
    except:
        print("Invalid values for year or month. The first available year is 2024.")
        return pd.DataFrame(), driver

    table_link = f"https://www.wunderground.com/dashboard/pws/{city_code}/table/{year_number}-{month_number}-01/{year_number}-{month_number}-31/monthly"

    if not driver:
        driver = webdriver.Chrome() 
        driver.maximize_window()
        driver.get(table_link)
        handle_cookies(driver)
    else:
        driver.get(table_link)
    
    return scrape_table(driver, city_code), driver

def scrape_table(driver, city_code):
    try:
        rows = driver.find_element("css selector", "#main-page-content > div > div > div > lib-history > div.history-tabs > lib-history-table > div > div").text.split("\n")
    except:
        print("Error retrieving the table rows.")
        return pd.DataFrame()

    df_table = pd.Series([row.replace("°F", "").replace("%", "").replace("mph", "").replace("in", "") for row in rows])
    df_table = df_table.str.split(expand=True)
    df_table.columns = df_table.iloc[1]
    df_table = df_table[2:]
    df_table["Date"] = pd.to_datetime(df_table["Date"])
    df_table.columns = ['Date', 'Temp High ºF', 'Temp Avg ºF', 'Temp Low ºF', 'Dew High ºF', 'Dew Avg ºF', 'Dew Low ºF',
                        'Humid High %', 'Humid Avg %', 'Humid Low %', 'Speed High mph', 'Speed Avg mph', 'Speed Low mph', 
                        'Pressure High in', 'Pressure Low in', 'Precip Sum in']
    df_table["city_code"] = city_code
    return df_table

def random_cities_and_scrape_tables(n_cities, cities_df, n_months=1, start_year=2024, start_month=1):
    random_cities = cities_df.sample(n=n_cities)

    cities_with_codes = random_cities[~random_cities["code_wunder"].isna()]
    cities_without_codes = random_cities[random_cities["code_wunder"].isna() | random_cities["code_wunder"].eq("")]

    df_final = pd.DataFrame()

    with ThreadPoolExecutor(max_workers=5) as executor:
        for city_code in cities_with_codes["code_wunder"].to_list():
            for month in range(start_month, start_month + n_months):
                future = executor.submit(get_city_table_df, city_code, start_year, month)
                future_to_city[future] = city_code

        future_to_city = {}
        for city_name in cities_without_codes["city"].to_list():
            future = executor.submit(scrape_city_code, city_name)
            future_to_city[future] = city_name

        for future in as_completed(future_to_city):
            city_name = future_to_city[future]
            try:
                city_code = future.result()
                print(f"Scraped city code for {city_name}: {city_code}")
                cities_df.loc[cities_df['city'] == city_name, "code_wunder"] = city_code
                for month in range(start_month, start_month + n_months):
                    df, driver = get_city_table_df(city_code, start_year, month)
                    df_final = pd.concat([df_final, df], axis=0)
            except:
                print(f"Error scraping city {city_name}")

    df_final.to_csv("../data/historical_weather_saved_concurrent.csv")
    return df_final
