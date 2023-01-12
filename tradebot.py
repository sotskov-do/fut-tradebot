from collections import Counter
import os
from random import choice
from statistics import median, mode, mean
import time

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException

from navigation import *
from user_agents import ua
from xpaths import PLAYERS_TO_LIST_XPATH


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

def determine_min_buyout_price(driver: WebDriver, section=None, pages_to_scan=10) -> None: #, player_name=None):
    # if player_name is None:
    #     compare_player_price(driver)
    # else:
    #     search_player(driver, player_name)
    # statistics.StatisticsError: no median for empty data
    buyout_price_list_total = []
    # while True:
    for _ in range(pages_to_scan):
        time.sleep(0.75)

        while True:
            try:
                if section is None:
                    buyout_price_list = driver.find_elements(By.XPATH, '//div[@class="auctionValue"]//span[contains(@class, "value")]')
                else:
                    buyout_price_list = driver.find_elements(By.XPATH, f'{section}//div[@class="auctionValue"]//span[contains(@class, "value")]')
                buyout_price_list = [int(price.text.replace(" ", "").replace(",", "")) for price in buyout_price_list[1::2] if price.text.replace(" ", "").replace(",", "") != ""]
                break
            except StaleElementReferenceException:
                continue

        buyout_price_list_total.extend(buyout_price_list)
        if driver.find_element(By.XPATH, '//button[contains(@class, "next")]').get_attribute("style") == "display: none;":
            break
        else:
            go_next_page(driver)
    # TODO: choose correct price
    # TODO: price to calculate depends from amount of founded players
    # print("dict -", Counter(buyout_price_list_total))
    # print("median -", median(buyout_price_list_total))
    # print("mode -", mode(buyout_price_list_total))
    # go_main_page(driver)
    return mean(sorted(buyout_price_list_total)[:5]) * 0.95
    # return median(buyout_price_list_total) * 0.925


def list_on_transfer_market(driver: WebDriver, price: int) -> None:
    click_button(driver, '//div[@class="ut-quick-list-panel-view"]')
    bid = driver.find_element(By.XPATH, '(//input[contains(@class, "ut-number-input-control")])[1]')
    bid.click()
    bid.send_keys(price)
    buyout = driver.find_element(By.XPATH, '(//input[contains(@class, "ut-number-input-control")])[2]')
    buyout.click()
    buyout.send_keys(price)
    click_button(driver, '(//button[contains(@class, "call-to-action")])[last()]')


def locate_player_in_transfer_pile(driver: WebDriver) -> None:
    pass


def relist(driver: WebDriver) -> None:
    click_button(driver, '//button[text()="Re-list All" and not(@style="display: none;")]')
    time.sleep(1)
    click_button(driver, '//section[contains(@class, "ea-dialog-view-type--message")]//button[.//text()="Yes"]')

def remove_all_sold(driver: WebDriver) -> None:
    #TODO
    pass

def clear_sold(driver: WebDriver) -> None:
    click_button(driver, '//button[text()="Clear Sold" and not(@style="display: none;")]')


def list_players_in_transfer_pile(driver: WebDriver) -> None:
    scanned_players = dict()

    enter_transfer_list(driver)
    time.sleep(2.5)
    
    # TODO: remove all sold
    if len(driver.find_elements(By.XPATH, '//li[contains(@class, "won")]//div[@class="name"]')) > 1:
        remove_all_sold(driver)

    if len(driver.find_elements(By.XPATH, '//li[contains(@class, "expired")]//div[@class="name"]')) > 1:
        relist(driver)
    
    players_to_sell = driver.find_elements(By.XPATH, PLAYERS_TO_LIST_XPATH)
    players_names = [player_name.text for player_name in players_to_sell]
    # for player in players_to_sell:
    # FIXME: error if no other player on market
    print(len(players_to_sell))
    for idx in range(len(players_to_sell)):
        current_player_name = players_names[idx]
        print(current_player_name)
        print(scanned_players)
        if current_player_name in scanned_players:
            time.sleep(1.5)
            list_on_transfer_market(driver, current_player_price)
        else:
            # FIXME: sometimes click wrong player, maybe need delay
            time.sleep(1.5)
            click_button(driver, PLAYERS_TO_LIST_XPATH)

            action = webdriver.ActionChains(driver)
            element = driver.find_element(By.XPATH, '//div[@class="ut-quick-list-panel-view"]')
            action.move_to_element(element)
            # for i in range(50):
            #     action.move_by_offset(0, i)
            action.move_by_offset(0, 175)
            action.perform()
            click_button(driver, '//span[@class="btn-text" and text()="Compare Price"]/parent::button[@class]')

            current_player_price = determine_min_buyout_price(driver, section='//section[contains(@class, "ui-layout-right")]', pages_to_scan=15)
            print(current_player_price)
            click_button(driver, PLAYERS_TO_LIST_XPATH)
            # enter_transfer_list(driver)
            # click_button(driver, f'//div[@class="name" and text()="{player}"]')
            scanned_players[current_player_name] = current_player_price
            list_on_transfer_market(driver, current_player_price)


def create_driver() -> WebDriver:
    url = "https://www.ea.com/en-en/fifa/ultimate-team/web-app/"
    driver = SeleniumDriver().get_driver()
    
    while True:
        try:
            driver.get(url)
            break
        except WebDriverException:
            continue

    WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "call-to-action")]')))
    # btn = driver.find_element(By.XPATH, '//button[contains(@class, "call-to-action")]')
    btn = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "call-to-action")]')))
    btn.click()
    return driver


def login(driver: WebDriver) -> None:
    driver.find_element(By.XPATH, '//input[@id="email"]').send_keys(os.environ.get("EMAIL"))
    driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(os.environ.get("PSWD"))
    login_btn = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//a[@id="logInBtn"]')))
    login_btn.click()
    send_code_btn = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//a[@id="btnSendCode"]')))
    send_code_btn.click()
    print("You have 180 seconds to enter the code.")
    # TODO: enter code by input


def enter_transfer_market(driver: WebDriver) -> None:
    click_button(driver, '//button[contains(@class, "icon-transfer")]')
    click_button(driver, '//div[contains(@class, "ut-tile-transfer-market")]')


def enter_transfer_list(driver: WebDriver) -> None:
    click_button(driver, '//button[contains(@class, "icon-transfer")]')
    click_button(driver, '//div[contains(@class, "ut-tile-transfer-list")]')


def search_player(driver: WebDriver, player_name: str) -> None:
    enter_transfer_market(driver)
    driver.find_element(By.XPATH, '//input[@class="ut-text-input-control"]').send_keys(player_name)
    click_button(driver, '//ul[contains(@class, "playerResultsList")]/button')
    click_button(driver, '//button[contains(@class, "call-to-action")]')


if __name__ == "__main__":
    load_dotenv(".env")
    driver = create_driver()
    login(driver)
    WebDriverWait(driver, timeout=180).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "icon-transfer")]')))
    #TODO cli menu
    list_players_in_transfer_pile(driver)
    # enter_transfer_market(driver)
    # search_player(driver)
    # determine_min_buyout_price(driver, os.environ.get("PLAYER_TO_SEARCH"))
    # time.sleep(5)
    # go_back(driver)
    # time.sleep(600)
    driver.quit()
