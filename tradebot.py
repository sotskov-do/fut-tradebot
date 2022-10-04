from copy import deepcopy
import os
from random import choice
import time
from typing import List

from icecream import ic
import numpy as np
import pandas as pd
import openpyxl
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from tqdm import tqdm
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

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


def enter_transfers(driver):
    transfer_btn = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "icon-transfer")]')))
    transfer_btn.click()


if __name__ == "__main__":
    load_dotenv(".env")
    driver = create_driver()
    login(driver)
    WebDriverWait(driver, timeout=180).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "icon-transfer")]')))
    enter_transfers(driver)
    time.sleep(300)
