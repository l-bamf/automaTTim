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

product_options = {
    "original": "Tim Tam Original",
    "white": "Tim Tam White",
    "dark": "Tim Tam Dark",
    "double": "Tim Tam Double Coat",
    "chewy-caramel": "Tim Tam Chewy Caramel",
    "murray-caramel": "Tim Tam Murray River Salted Caramel"
}


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


def enter_product_details(driver, type) -> (bool, str):
    """
    Enter product details and upload correct file
    :param driver:
    :param type:
    :return:
    """
    time.sleep(1)  # TODO: Use selenium best practice wait
    mobile_field = driver.find_element(By.ID, "mobile")
    with open("details.json") as json_file:
        details = json.load(json_file)
        mobile_field.send_keys(details["mobile"])

    product_select = Select(driver.find_element(By.ID, "what_did_you_purchase"))
    product_select.select_by_value(product_options[type])

    shop_select = Select(driver.find_element(By.ID, "where_did_you_make_the_purchase"))
    shop_select.select_by_value("Coles-1")

    terms_box = driver.find_element(By.ID, "terms")
    terms_box.click()

    receipt_directories = os.listdir("receipts")
    parent_path = str(pathlib.Path().resolve()) + "\\receipts\\"
    if type != "original" and type in receipt_directories:
        receipt_directories = os.listdir("receipts\\" + type)
        parent_path += type + "\\"

    selected_receipt_path = None
    for receipt_dir in receipt_directories:
        if re.search(".JPG", receipt_dir):
            selected_receipt_path = parent_path + receipt_dir
            break

    file_input = driver.find_element(By.ID, "receipt_upload")
    file_input.send_keys(selected_receipt_path)
    time.sleep(5)

    upload_success = False
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
    country_select.select_by_value(details["country"] + "-1")

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


def move_receipt(receipt_path, type):
    """
    Move used receipt into a discarded folder
    :param receipt_path:
    :param type:
    :return:
    """
    now = datetime.now()
    parent_dir = str(pathlib.Path().resolve())
    now_str = now.strftime("%Y-%m-%d-%H.%M")
    file_name = receipt_path.split("\\")[-1]
    if type == "original":
        new_path = str(pathlib.Path().resolve()) + "\\receipts\\used_receipts\\" + now_str + "_" + file_name
    else:
        folder_path = "\\receipts\\used_receipts\\" + type
        os.makedirs(parent_dir + folder_path, exist_ok=True)
        new_path = parent_dir + folder_path + "\\" + now_str + "_" + file_name
    os.replace(receipt_path, new_path)


def full_flow(type="original"):
    global receipt_path
    service = Service('chromedriver_win32/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    success = False
    while not success:
        driver.get("https://www.timtam3wishes.com/enter")
        if not pass_checklist(driver):
            continue

        product_success, receipt_path = enter_product_details(driver, type)
        if not product_success:
            continue

        success = enter_personal_details(driver)
        time.sleep(2)

    # press the button!
    # enter_button = driver.find_element(By.XPATH, "//*[text()='Enter!']")
    # enter_button.click()
    # move_receipt(receipt_path, type)
    time.sleep(20)
    print("Form submitted")
    driver.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in product_options:
            full_flow(sys.argv[1])
        else:
            print("Invalid product type as argument - must be one of: ")
            print(product_options.keys())
            exit()
    else:
        full_flow()

