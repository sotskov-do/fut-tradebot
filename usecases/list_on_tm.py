import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from usecases.check_price import determine_min_buyout_price
from utils.navigation import click_button, enter_transfer_list
from xpaths import PLAYERS_TO_LIST_XPATH


def list_on_transfer_market(driver: WebDriver, price: int) -> None:
    click_button(driver, '//div[@class="ut-quick-list-panel-view"]')
    bid = driver.find_element(By.XPATH, '(//input[contains(@class, "ut-number-input-control")])[1]')
    bid.click()
    bid.send_keys(price)
    buyout = driver.find_element(By.XPATH, '(//input[contains(@class, "ut-number-input-control")])[2]')
    buyout.click()
    buyout.send_keys(price)
    click_button(driver, '(//button[contains(@class, "call-to-action")])[last()]')


def relist_pile(driver: WebDriver) -> None:
    click_button(driver, '//button[text()="Re-list All" and not(@style="display: none;")]')
    time.sleep(1)
    click_button(driver, '//section[contains(@class, "ea-dialog-view-type--message")]//button[.//text()="Yes"]')


def clear_sold(driver: WebDriver) -> None:
    click_button(driver, '//button[text()="Clear Sold" and not(@style="display: none;")]')


def list_players_in_transfer_pile(driver: WebDriver, relist=True) -> None:
    scanned_players = dict()

    enter_transfer_list(driver)
    
    # TODO: remove all sold
    if len(driver.find_elements(By.XPATH, '//li[contains(@class, "won")]//div[@class="name"]')) > 1:
        clear_sold(driver)

    if len(driver.find_elements(By.XPATH, '//li[contains(@class, "expired")]//div[@class="name"]')) > 1 and relist:
        relist_pile(driver)

    time.sleep(2.5)
    
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