from requests.models import Response
from selenium.common import exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import random
import secret
import requests
def get_item(URL):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.execute_script("window.open('"+URL+"');")
    driver.close()
    driver.switch_to.window(window_name=driver.window_handles[0])
    button = driver.find_element_by_css_selector("button[data-button-state='ADD_TO_CART']")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-button-state='ADD_TO_CART']")))
    Active = True
    while Active:
        driver.execute_script("arguments[0].click();", button)
        try:
            time.sleep(1)
            driver.find_element_by_css_selector("a[aria-label='Cart, 1 item']")
            Active = False
        except:
            time.sleep(random.randrange(1, 3))
    driver.execute_script("window.open('https://www.bestbuy.com/checkout/r/fulfillment');")
    driver.close()
    driver.switch_to.window(window_name=driver.window_handles[0])
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[1]/div/div/section/div[2]/div[1]/section/section/div[1]/label/div/input")))
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[1]/div/div/section/div[2]/div[1]/section/section/div[1]/label/div/input").send_keys(secret.first_name)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[1]/div/div/section/div[2]/div[1]/section/section/div[2]/label/div/input").send_keys(secret.last_name)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[1]/div/div/section/div[2]/div[1]/section/section/div[3]/div[2]/div/div/input").send_keys(secret.address)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[1]/div/div/section/div[2]/div[1]/section/section/div[5]/div/div[1]/label/div/input").send_keys(secret.city)
    selectstate = driver.find_element_by_class_name('tb-select')
    for option in selectstate.find_elements_by_tag_name('option'):
        if option.text == secret.state:
            option.click()
            break
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[1]/div/div/section/div[2]/div[1]/section/section/div[6]/div/div[1]/label/div/input").send_keys(secret.zip_code)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[2]/div/section/div[2]/label/div/input").send_keys(secret.email)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[2]/div/section/div[3]/label/div/input").send_keys(secret.phone_number)
    driver.find_element_by_class_name("btn.btn-lg.btn-block.btn-secondary").click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[3]/div/section/div[1]/div[1]/div/section/div[1]/div/input")))
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[3]/div/section/div[1]/div[1]/div/section/div[1]/div/input").send_keys(secret.card_number)
    selectmonth = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[3]/div/section/div[1]/div[1]/div/section/div[2]/div[1]/div/div[1]/label/div/div/select")
    for option in selectmonth.find_elements_by_tag_name('option'):
        if option.text == secret.exp_month:
            option.click()
            break
    selectyear = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[3]/div/section/div[1]/div[1]/div/section/div[2]/div[1]/div/div[2]/label/div/div/select")
    for option in selectyear.find_elements_by_tag_name('option'):
        if option.text == secret.exp_year:
            option.click()
            break
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[3]/div/section/div[1]/div[1]/div/section/div[2]/div[2]/div/div[2]/div/input").send_keys(secret.security_code)
    driver.find_element_by_class_name("btn.btn-lg.btn-block.btn-primary").click()
    time.sleep(5)
get_item(URL = requests.get("http://159.223.142.24:5000/main").text)
