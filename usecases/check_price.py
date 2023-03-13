from statistics import median, mode, mean
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException

from utils.navigation import go_next_page


def determine_min_buyout_price(driver: WebDriver, section=None, pages_to_scan=10) -> None: #, player_name=None):
    # if player_name is None:
    #     compare_player_price(driver)
    # else:
    #     search_player(driver, player_name)
    # statistics.StatisticsError: no median for empty data
    buyout_price_list_total = []
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
    # TODO: price if no player found
    # go_main_page(driver)
    return mean(sorted(buyout_price_list_total)[:5]) * 0.975
    # return median(buyout_price_list_total) * 0.925