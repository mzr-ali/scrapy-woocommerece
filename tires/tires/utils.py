import os
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']
SCRAPING_URL = os.environ['SCRAPING_URL']
DOMAIN = os.environ['DOMAIN']

HOST_URL = os.environ['HOST_URL']
C_KEY = os.environ['CONSUMER_KEY']
S_KEY = os.environ['SECRECT_KEY']


def spect_table(specs_dic):
    table = '<TABLE  border=0 cellSpacing=0 cellPadding=0 width="100%">'
    table_end = '</table>'
    tbody = "<tbody>"
    tbody_end = "</tbody>"
    tr = ""
    for k, v in specs_dic.items():
        tr += f"<tr><td width=131 >{k}</td><td width=365>{v}</td></td></tr>"
    return f'{table}{tbody}{tr}{tbody_end}{table_end}'


def login(driver, user=None, password=None, cookie=True, timeout=10):
    # if cookie:
    #     if cookie_exists():
    #         return _login_with_cookie(driver)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username_login")))

    email_elem = driver.find_element(By.ID, "username_login")
    email_elem.clear()
    action_chains = ActionChains(driver)
    action_chains.move_to_element(email_elem).click().perform()
    email_elem.send_keys(user)
    time.sleep(2)

    hidden = driver.find_element(By.CSS_SELECTOR, "input.hidden-input")
    action_chains = ActionChains(driver)
    action_chains.move_to_element(hidden).click().perform()
    time.sleep(2)
    password_elem = driver.find_element(By.ID, "password_login")
    password_elem.send_keys(password)
    time.sleep(2)

    validate = driver.find_element(By.CLASS_NAME, "submitLanding")

    validate.click()

    try:
        element = WebDriverWait(driver, 30).until(
            lambda driver: driver.find_element(By.CSS_SELECTOR, 'img.d-md-block'))

    except:
        pass
    return driver


def remove_tag(description):
    if description:
        description = description.strip()
        description = description.replace('+', '')
        description = description.replace('\t', '')
        description = description.replace('\n', '')
        description = description.encode('ascii', 'ignore')
        description = description.decode()
        return description


def price_increase(price):
    price = float(price.replace(',', '.'))
    increased = price + (price * 0.5)
    p = '{:.2f}'.format(increased)
    return str(p).replace(".", ",")
