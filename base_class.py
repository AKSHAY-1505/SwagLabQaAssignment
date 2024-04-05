from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

class BaseClass:

    def __init__(self,driver):
        self.driver = driver

    def get_by_xpath(self, xpath):
        ele = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return ele

    def open_page(self):
        self.driver.get("https://www.saucedemo.com/")
        self.driver.maximize_window()

    def get_valid_usernames(self):
        usernames_div = self.get_by_xpath('//div[@id="login_credentials"]')

        text = usernames_div.text

        usernames = text.split("\n")

        usernames.remove('Accepted usernames are:')

        print(f"\nAccepted User Names: {usernames}")

        return usernames

    def get_valid_password(self):
        passwords_div = self.get_by_xpath("//div[@id='login_credentials']/following-sibling::div")

        text = passwords_div.text

        passwords = text.split("\n")

        passwords.remove('Password for all users:')

        print(f"\nAccepted Password: {passwords[0]}")

        return passwords[0]

    def login(self,username,password):
        username_field = self.get_by_xpath("//input[@id='user-name']")
        password_field = self.get_by_xpath("//input[@id='password']")
        login_button = self.get_by_xpath("//input[@id='login-button']")

        username_field.clear()
        username_field.send_keys(username)

        password_field.clear()
        password_field.send_keys(password)
        login_button.click()

    def logout(self):
        menu_button = self.get_by_xpath("//button[@id='react-burger-menu-btn']")
        menu_button.click()

        log_out_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='logout_sidebar_link']")))
        log_out_button.click()
    def validate_login(self,username,password):
        self.login(username,password)

        try:
            self.get_by_xpath("//button[@id='react-burger-menu-btn']")
            self.logout()
            return True
        except:
            return False

    def validate_all_combinations(self,usernames,password):
        rejected_combos = []

        for username in usernames:
            if self.validate_login(username, password):
                continue
            else:
                rejected_combos.append(username)

        if len(rejected_combos) == 0:
            print("All combinations work")
        else:
            print(f"\nUsernames failed in Login: {rejected_combos}")


    def filter_price_high_to_low(self):
        filter_dropdown = self.get_by_xpath("//option[text()='Name (A to Z)']//parent::select")
        filter_dropdown.click()

        high_to_low_option = self.get_by_xpath("//option[contains(text(),'low to high')]")
        high_to_low_option.click()

    def get_third_highest_price(self):
        element = self.get_by_xpath("//div[@class='inventory_item'][3]//div[@class='inventory_item_price']")
        price = element.text
        print(f"\nThird Highest Price in the Store: {price}")

    def print_details(self,details):
        print("\nThird Highest Apparel Details:")
        for key in details:
            print(f"{key}: {details[key]}")

    def get_third_highest_apparel_details(self):
        self.filter_price_high_to_low()

        apparel = self.get_by_xpath("//div[@class='inventory_item'][3]")

        text = apparel.text

        list_of_details = text.split("\n")
        details = {}

        details['Name'] = list_of_details[0]
        details['Description'] = list_of_details[1]
        details['Price'] = list_of_details[2]

        self.print_details(details)
