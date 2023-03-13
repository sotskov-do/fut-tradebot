import os

from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webdriver import WebDriver

from utils.navigation import *


from driver import create_driver
from usecases.list_on_tm import list_players_in_transfer_pile
from usecases.snipe import snipe


def login(driver: WebDriver) -> None:
    driver.find_element(By.XPATH, '//input[@id="email"]').send_keys(os.environ.get("EMAIL"))
    driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(os.environ.get("PSWD"))
    login_btn = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//a[@id="logInBtn"]')))
    login_btn.click()
    send_code_btn = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//a[@id="btnSendCode"]')))
    send_code_btn.click()
    print("You have 180 seconds to enter the code.")
    # TODO: enter code by input


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
