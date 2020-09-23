# -*- coding: utf8 -*-

# selen_scraper.py
# Dani Suarez - suarezdanieltomas@gmail.com

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import re


def open_firefox():
    '''
    '''
    print('Opening Firefox...\n')
    driver = webdriver.Firefox()
    return driver


def get_price(url, driver, change_zip_code=False):
    '''
    Returns the price of a product from
    an amazon.com page. Kinda hardcoded.
    '''
    driver.get(url)

    # ZIP Code change
    if change_zip_code:
        sleep(3)
        change_address = driver.find_element_by_css_selector('span.a-spacing-top-base:nth-child(2) > span:nth-child(1) > input:nth-child(1)')
        change_address.click()
        sleep(2)
        zip_update = driver.find_element_by_css_selector('#GLUXZipUpdateInput')
        zip_update.send_keys('33101')
        apply = driver.find_element_by_css_selector('#GLUXZipUpdate > span:nth-child(1) > input:nth-child(1)')
        apply.click()
        sleep(2)
        continue_button = driver.find_element_by_css_selector('.a-popover-footer > span:nth-child(1) > span:nth-child(1) > input:nth-child(1)')
        continue_button.click()
        sleep(2)

    body = driver.find_element_by_css_selector('body')
    body.send_keys(Keys.CONTROL + 'a')
    body.send_keys(Keys.CONTROL + 'c')
    text = pyperclip.paste()

    # price regex: "Price: \t$1,574.00"
    price_regex = re.compile(r'(\nPrice: \t\$)([0-9,.])+')  # In chrome that
    price_search = price_regex.search(text)          # space doesn't appear
    price = price_search.group(0)  # raw
    try:
        price = price.strip('\nPrice: \t$').replace(',', '')
    except ValueError:
        pass
    print(f'The price of "{driver.title}" is US ${price}\n')
    return price


def close_firefox(driver):
    print('Closing Firefox...\n')
    driver.quit()

'''
I need to clean the regex
'''