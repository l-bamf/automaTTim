"""
File automates the entry into the Arnotts TimTam 3 wishes competition through the web form.
This file is NOT concerned with timing the entry.
"""

import pprint
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pathlib
import json
from datetime import datetime
import sys
import re

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

product_options = {
    "original": "Tim Tam Original",
    "white": "Tim Tam White",
    "dark": "Tim Tam Dark",
    "double": "Tim Tam Double Coat",
    "chewy-caramel": "Tim Tam Chewy Caramel",
    "murray-caramel": "Tim Tam Murray River Salted Caramel"
}

retailer_options = {
    "coles": "Coles-1",
    "woolworths": "Woolworths-1",
    "iga": "IGA",
    "countdown": "Countdown-1",
    "new-world": "New World-1",
    "paknsave": "Pak'nSave",
    "other": "Other-3"
}

accepted_file_types = (".JPG", ".PDF", ".PNG", ".JPEG")

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
        if button.text.upper() == "GOT IT!":
            button.click()
            return True


def enter_product_details(driver) -> (bool, str):
    """
    Enter product details and upload correct file
    :param driver:
    :return:
    """
    time.sleep(1)  # TODO: Use selenium best practice wait
    mobile_field = driver.find_element(By.ID, "mobile")
    with open("details.json") as json_file:
        details = json.load(json_file)
        mobile_field.send_keys(details["mobile"])


    terms_box = driver.find_element(By.ID, "terms")
    terms_box.click()

    upload_success = False
    selected_receipt_path, flavour, retailer = find_receipt()

    if selected_receipt_path:
        product_select = Select(driver.find_element(By.ID, "what_did_you_purchase"))
        product_select.select_by_value(product_options[flavour])

        shop_select = Select(driver.find_element(By.ID, "where_did_you_make_the_purchase"))
        shop_select.select_by_value(retailer_options[retailer])

        file_input = driver.find_element(By.ID, "receipt_upload")
        file_input.send_keys(selected_receipt_path)
        # wait until the upload completes, either successfully or not, timeout after 30 seconds
        wait = WebDriverWait(driver, 30)
        wait.until(lambda driver: driver.find_element(By.XPATH, "//*[text()='Upload complete']") or
                                  driver.find_element(By.CSS_SELECTOR,
                                     "button[class='cursor-pointer text-input-active hover:underline focus:ring-2 focus:ring-input-active file-upload-browse']"))

        try:
            driver.find_element(By.XPATH, "//*[text()='Upload complete']")
        except NoSuchElementException:
            print("Upload failed!")
            reset_button = driver.find_element(By.CSS_SELECTOR,
                                     "button[class='cursor-pointer text-input-active hover:underline focus:ring-2 focus:ring-input-active file-upload-browse']")
            reset_button.click()
        else:
            print("Upload succeeded")
            upload_success = True

    return upload_success, selected_receipt_path


def find_receipt() -> (str, str, str):
    """
    Finds a receipt file, its flavour and retailer
    :return:
    """
    flavours = os.listdir("receipts")
    flavours.remove(".gitignore")
    flavours.remove("used_receipts")
    file_types_regex = "(.PNG|.JPG|.PDF|.JPEG)"
    selected_receipt_path = None
    selected_flavour = None
    for flavour in flavours:
        sub_dirs = [dir for dir in os.listdir("receipts\\" + flavour)]
        valid_receipts = [sub_dir for sub_dir in sub_dirs if re.search(file_types_regex, sub_dir.upper())]
        if len(valid_receipts) >= 1:
            parent_path = str(pathlib.Path().resolve()) + "\\receipts\\" + flavour + "\\"
            selected_receipt_path = parent_path + valid_receipts.pop()
            selected_flavour = flavour
            break
    receipt_retailer = "coles"  # default retailer
    for retailer in retailer_options.keys():
        if retailer in selected_receipt_path:
            receipt_retailer = retailer
            break
    return selected_receipt_path, selected_flavour, receipt_retailer


def enter_personal_details(driver):
    """
    Enter personal details if mobile number is unrecognised
    :param driver:
    :return:
    """
    try:
        driver.find_element(By.XPATH, "//*[text()='Your Details']")
    except NoSuchElementException:
        return True  # this step isn't necessary

    details = {}
    with open('details.json') as json_file:
        details = json.load(json_file)
    assert len(details) > 0

    fname_input = driver.find_element(By.ID, "first_name")
    fname_input.send_keys(details["first_name"])

    lname_input = driver.find_element(By.ID, "last_name")
    lname_input.send_keys(details["last_name"])

    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(details["email"])

    dob_input = driver.find_element(By.ID, "date_of_birth")
    dob_input.send_keys(details["dob"])

    country_select = Select(driver.find_element(By.ID, "country"))
    country_select.select_by_value(details["country"])

    st_address = driver.find_element(By.ID, "address_line_1")
    st_address.send_keys(details["st_address"])

    postcode_input = driver.find_element(By.ID, "postcode")
    postcode_input.send_keys(details["postcode"])

    suburb_input = driver.find_element(By.ID, "suburb")
    suburb_input.send_keys(details["suburb"])

    state_input = driver.find_element(By.ID, "state_or_region")
    state_input.send_keys(details["state"])

    confirm_box = driver.find_element(By.ID, "confirm_details")
    confirm_box.click()

    delivery = driver.find_element(By.ID, "prize_delivery_sms")
    delivery.click()

    return True


def move_receipt(receipt_path):
    """
    Move used receipt into a discarded folder
    :param receipt_path:
    :return:
    """
    now = datetime.now()
    parent_dir = str(pathlib.Path().resolve())
    now_str = now.strftime("%Y-%m-%d-%H.%M")
    file_name = receipt_path.split("\\")[-1]
    flavour = receipt_path.split("\\")[-2]

    folder_path = "\\receipts\\used_receipts\\" + flavour
    os.makedirs(parent_dir + folder_path, exist_ok=True)
    new_path = parent_dir + folder_path + "\\" + now_str + "_" + file_name
    os.replace(receipt_path, new_path)


def full_flow():
    global receipt_path
    service = Service('chromedriver_win32/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    success = False
    attempts = 0
    while not success and attempts < 10:
        driver.get("https://www.timtam3wishes.com/enter")
        if not pass_checklist(driver):
            continue

        product_success, receipt_path = enter_product_details(driver)
        if not product_success:
            attempts += 1
            continue

        success = enter_personal_details(driver)
        time.sleep(2)

    # press the button!
    enter_button = driver.find_element(By.XPATH, "//*[text()='Enter!']")
    enter_button.click()
    move_receipt(receipt_path)
    time.sleep(10)
    print("Form submitted")
    driver.close()

if __name__ == "__main__":
    if not find_receipt()[0]:
        print("No valid receipt found")
    else:
        full_flow()
