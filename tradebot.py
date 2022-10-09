from collections import Counter
import os
from random import choice
from statistics import median, mode
import time

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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


def go_back_main(driver):
    click_button(driver, '//button[@class="ut-navigation-button-control"]')


def go_back_last(driver):
    click_button(driver, '(//button[@class="ut-navigation-button-control"])[last()]')


def go_next_page(driver):
    click_button(driver, '//button[contains(@class, "next")]')


def go_main_page(driver):
    click_button(driver, '//button[contains(@class, "icon-home")]')


def determine_min_buyout_price(driver, section=None): #, player_name=None):
    # if player_name is None:
    #     compare_player_price(driver)
    # else:
    #     search_player(driver, player_name)
    buyout_price_list_total = []
    while True:
        if driver.find_element(By.XPATH, '//button[contains(@class, "next")]').get_attribute("style") == "display: none;":
            break
        time.sleep(2)
        # TODO:
        # selenium.common.exceptions.StaleElementReferenceException: Message: The element reference of <span class="currency-coins value"> is stale; 
        # either the element is no longer attached to the DOM, it is not in the current frame context, or the document has been refreshed
        if section is None:
            buyout_price_list = driver.find_elements(By.XPATH, '//div[@class="auctionValue"]//span[contains(@class, "value")]')
        else:
            buyout_price_list = driver.find_elements(By.XPATH, f'{section}//div[@class="auctionValue"]//span[contains(@class, "value")]')
        buyout_price_list = [int(price.text.replace(" ", "").replace(",", "")) for price in buyout_price_list[1::2] if price.text.replace(" ", "").replace(",", "") != ""]
        buyout_price_list_total.extend(buyout_price_list)
        go_next_page(driver)
    # TODO: choose correct price
    print("dict -", Counter(buyout_price_list_total))
    print("median -", median(buyout_price_list_total))
    print("mode -", mode(buyout_price_list_total))
    # go_main_page(driver)
    return median(buyout_price_list_total) * 0.95


def list_on_transfer_market(driver, price):
    click_button(driver, '//div[@class="ut-quick-list-panel-view"]')
    bid = driver.find_element(By.XPATH, '(//input[contains(@class, "ut-number-input-control")])[1]')
    bid.click()
    bid.send_keys(price)
    buyout = driver.find_element(By.XPATH, '(//input[contains(@class, "ut-number-input-control")])[2]')
    buyout.click()
    buyout.send_keys(price)
    time.sleep(60)
    click_button(driver, '(//button[contains(@class, "call-to-action")])[last()]')


def locate_player_in_transfer_pile(driver):
    pass


def list_players_in_transfer_pile(driver):
    enter_transfer_list(driver)
    time.sleep(2.5)
    players_to_sell = driver.find_elements(By.XPATH, '//li[contains(@class, "listFUTItem")]//div[@class="name"]')
    # for player in players_to_sell:
    for idx, player in enumerate(players_to_sell[:2]):
        if idx == 0:
            pass
        else:
            while True:
                try:
                    player.click()
                    break
                except ElementClickInterceptedException:
                    continue
            
        click_button(driver, '//span[@class="btn-text" and text()="Compare Price"]/parent::button[@class]') # FIXME: can't locate correctly without hover it manually 
        # player_price = determine_min_buyout_price(driver, section='//section[contains(@class, "ui-layout-right")]')
        player_price = 1615.0
        print(player_price)
        go_back_last(driver)
        # enter_transfer_list(driver)
        # click_button(driver, f'//div[@class="name" and text()="{player}"]')
        list_on_transfer_market(driver, player_price)


def create_driver(): 
    url = "https://www.ea.com/en-en/fifa/ultimate-team/web-app/"
    driver = SeleniumDriver().get_driver()
    
    # TODO:
    # selenium.common.exceptions.WebDriverException: Message: Reached error page:
    driver.get(url)

    WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "call-to-action")]')))
    # btn = driver.find_element(By.XPATH, '//button[contains(@class, "call-to-action")]')
    btn = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "call-to-action")]')))
    btn.click()
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


def enter_transfer_list(driver):
    click_button(driver, '//button[contains(@class, "icon-transfer")]')
    click_button(driver, '//div[contains(@class, "ut-tile-transfer-list")]')


def search_player(driver, player_name):
    enter_transfer_market(driver)
    driver.find_element(By.XPATH, '//input[@class="ut-text-input-control"]').send_keys(player_name)
    click_button(driver, '//ul[contains(@class, "playerResultsList")]/button')
    click_button(driver, '//button[contains(@class, "call-to-action")]')


if __name__ == "__main__":
    load_dotenv(".env")
    driver = create_driver()
    login(driver)
    WebDriverWait(driver, timeout=180).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "icon-transfer")]')))
    list_players_in_transfer_pile(driver)
    # enter_transfer_market(driver)
    # search_player(driver)
    # determine_min_buyout_price(driver, os.environ.get("PLAYER_TO_SEARCH"))
    # time.sleep(5)
    # go_back(driver)
    # time.sleep(600)
    driver.quit()
