from random import choice

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException


from utils.user_agents import ua


URL = "https://www.ea.com/en-en/fifa/ultimate-team/web-app/"


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


def create_driver() -> WebDriver:
    driver = SeleniumDriver().get_driver()
    
    while True:
        try:
            driver.get(URL)
            break
        except WebDriverException:
            continue

    WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "call-to-action")]')))
    btn = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "call-to-action")]')))
    btn.click()
    return driver