from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def click_button(driver: WebDriver, xpath: str) -> None:
    # TODO: update for created buttons
    while True:
        try:
            btn = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            btn.click()
            break
        except ElementClickInterceptedException:
            continue
        except StaleElementReferenceException:
            continue

def go_back_main(driver: WebDriver):
    click_button(driver, '//button[@class="ut-navigation-button-control"]')


def go_back_last(driver: WebDriver):
    click_button(driver, '(//button[@class="ut-navigation-button-control"])[last()]')


def go_next_page(driver: WebDriver):
    click_button(driver, '//button[contains(@class, "next")]')


def go_main_page(driver: WebDriver):
    click_button(driver, '//button[contains(@class, "icon-home")]')