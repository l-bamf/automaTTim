"""
File automates the entry into the Arnotts TimTam 3 wishes competition through the web form.
This file is NOT concerned with timing the entry.
"""

import pprint
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

PHONE = '0499111222'


def pass_checklist(driver):
    """
    When the page opens a number of check-boxes need to be checked to proceed.
    :param driver: chrome web-driver
    :return:
    """
    # Retrieves all check-boxes, including an inaccessible one (used in next step_
    check_boxes = driver.find_elements(By.CSS_SELECTOR,
                                 "input[class='cursor-pointer peer absolute left-0 top-0 opacity-0 w-5 h-5']")
    # Click all of them
    for elem in check_boxes:
        try:
            elem.click()
        except:
            pass

    # Get all buttons and click correct one
    buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
    for button in buttons:
        if button.accessible_name == "GOT IT!":
            button.click()

    print("Checklist step passed!")


def enter_details(driver):
    time.sleep(0.5) # TODO: Use best practice wait
    mobile_field = driver.find_element(By.CSS_SELECTOR, "input[id='mobile']")
    mobile_field.send_keys(PHONE)
    mobile_field.send_keys(Keys.TAB)
    pass


if __name__ == "__main__":
    service = Service('chromedriver_win32/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.timtam3wishes.com/enter")

    pass_checklist(driver)
    enter_details(driver)

    driver.close()

