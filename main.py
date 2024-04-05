from selenium import webdriver

from base_class import BaseClass

def main():
    driver = webdriver.Chrome()

    base = BaseClass(driver)

    base.open_page()

    usernames = base.get_valid_usernames()

    password = base.get_valid_password()

    base.validate_all_combinations(usernames,password)

    base.login(usernames[0],password)

    base.filter_price_high_to_low()

    base.get_third_highest_price()

    base.get_third_highest_apparel_details()




if __name__ == "__main__":
    main()