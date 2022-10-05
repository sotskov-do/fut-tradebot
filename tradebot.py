import os
from random import choice
import time

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import ElementClickInterceptedException

from user_agents import ua

class SeleniumDriver():
    def __init__(self):
        self.opts = Options()
        self.service = Service(executable_path="geckodriver.exe")
    
    def set_options(self):
        # self.opts.add_argument("--headless")
        # self.opts.add_argument("--width=800")
        # self.opts.add_argument("--height=600")
        self.opts.set_preference("general.useragent.override", choice(ua))

    def get_driver(self):
        self.set_options()
        self.driver = webdriver.Firefox(service=self.service, options=self.opts)
        return self.driver


def click_button(driver, xpath):
    while True:
        try:
            btn = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            btn.click()
            break
        except ElementClickInterceptedException:
            continue


def go_back(driver):
    click_button(driver, '//button[@class="ut-navigation-button-control"]')


def go_next_page(driver):
    click_button(driver, '//button[contains(@class, "next")]')


def determine_min_buyout_price(driver):
    buyout_price_list = driver.find_elements(By.XPATH, '//div[@class="auctionValue"]//span[contains(@class, "value")]')
    buyout_price_list = [int(price.text.replace(" ", "")) for price in buyout_price_list[1::2]]
    print(min(buyout_price_list))


def create_driver(): 
    url = "https://www.ea.com/ru-ru/fifa/ultimate-team/web-app/"
    driver = SeleniumDriver().get_driver()

    driver.get(url)

    WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "call-to-action")]')))
    # btn = driver.find_element(By.XPATH, '//button[contains(@class, "call-to-action")]')
    btn = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "call-to-action")]')))
    btn.click()
    btn.send_keys
    return driver


def login(driver):
    driver.find_element(By.XPATH, '//input[@id="email"]').send_keys(os.environ.get("EMAIL"))
    driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(os.environ.get("PSWD"))
    login_btn = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//a[@id="logInBtn"]')))
    login_btn.click()
    send_code_btn = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//a[@id="btnSendCode"]')))
    send_code_btn.click()
    print("You have 180 seconds to enter the code.")


def enter_transfer_market(driver):
    click_button(driver, '//button[contains(@class, "icon-transfer")]')
    click_button(driver, '//div[contains(@class, "ut-tile-transfer-market")]')


def search_player(driver):
    driver.find_element(By.XPATH, '//input[@class="ut-text-input-control"]').send_keys(os.environ.get("PLAYER_TO_SEARCH"))
    click_button(driver, '//ul[contains(@class, "playerResultsList")]/button')
    click_button(driver, '//button[contains(@class, "call-to-action")]')


if __name__ == "__main__":
    load_dotenv(".env")
    driver = create_driver()
    login(driver)
    WebDriverWait(driver, timeout=180).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "icon-transfer")]')))
    enter_transfer_market(driver)
    search_player(driver)
    determine_min_buyout_price(driver)
    time.sleep(5)
    go_back(driver)
    time.sleep(600)
    driver.quit()
