from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from utils.navigation import click_button, enter_transfer_market


def search_player(driver: WebDriver, player_name: str) -> None:
    enter_transfer_market(driver)
    driver.find_element(By.XPATH, '//input[@class="ut-text-input-control"]').send_keys(player_name)
    click_button(driver, '//ul[contains(@class, "playerResultsList")]/button')
    click_button(driver, '//button[contains(@class, "call-to-action")]')


def snipe(driver: WebDriver) -> None:
    pass