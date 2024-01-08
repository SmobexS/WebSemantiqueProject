from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time

def get_price(url):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("start-maximized")

    chrome_options.set_capability("browserVersion", "117")
    

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        time.sleep(3)

        try :
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "cart"))
            )

            cart_html = driver.find_element(By.ID, "cart").get_attribute("outerHTML")

            soup = BeautifulSoup(cart_html, 'html.parser')

            price_span = soup.find('span', class_='cart-heading--title-or-errors')
            verification = price_span.find('small')
            if verification is not None:
                price_re = re.findall(r'(\d+,\d+)', verification.text)
                str_price = price_re[0]
                price = str_price.replace(',','.')
            else:
                str_price = re.findall(r'(\d+,\d+)',price_span.text)[0]
                price = str_price.replace(',','.')

            driver.quit()

            return float(price)
        except :

            driver.quit()

            return None
    except:
        driver.quit()
        return None