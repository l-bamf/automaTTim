# pip install selenium

import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def pass_checklist(driver):
    check_boxes = driver.find_elements(By.CSS_SELECTOR,
                                 "input[class='cursor-pointer peer absolute left-0 top-0 opacity-0 w-5 h-5']")
    for elem in check_boxes:
        try:
            elem.click()
        except:
            pass
    buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
    for button in buttons:
        if button.accessible_name == "GOT IT!":
            button.click()

    print("Checklist step passed!")


if __name__ == "__main__":
    service = Service('chromedriver_win32/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.timtam3wishes.com/enter")

    pass_checklist(driver)

