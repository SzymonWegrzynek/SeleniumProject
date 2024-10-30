from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CookieClicker:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()

    
    def open_window(self) -> str:
        self.driver.get("https://orteil.dashnet.org/cookieclicker/")
        self.driver.maximize_window()
        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'fc-button-label')))
        return "Window opened and maximized"
    

    def accept_personal_data(self) -> str:
        personal_data_confirm = self.driver.find_element(By.CLASS_NAME, 'fc-button-label')
        personal_data_confirm.click()
        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, 'cc_btn_accept_all')))
        return "Personal data accepted"


    def accept_cookies(self) -> str:
        accept_cookies = self.driver.find_element(By.CLASS_NAME, 'cc_btn_accept_all')
        accept_cookies.click()
        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.ID, 'langSelect-PL')))
        return "Cookies accepted"


    def set_language(self) -> str:
        select_language = self.driver.find_element(By.ID, 'langSelect-PL')
        select_language.click()
        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, 'bigCookie')))
        return "Set language"


    def click_cookie(self) -> None:
        cookie = self.driver.find_element(By.ID, 'bigCookie')
        cookie.click()


    def get_cookies_amount(self) -> str:
        cookie_amount = self.driver.find_element(By.ID, 'cookies').text
        return cookie_amount
    

    def close_window(self) -> str:
        self.driver.close()
        return "Window closed"
    

    def buy_upgrade(self) -> list:
        upgrades_to_buy = self.driver.find_elements(By.CSS_SELECTOR, '.crate.upgrade.enabled')

        if upgrades_to_buy:
            for upgrade in upgrades_to_buy:
                upgrade.click()  
                print(f"An upgrade has been purchased: {upgrade}") 
        else:
            print("No improvements available for purchase")

        return upgrades_to_buy
    

    def buy_building(self) -> list:
        buildings_to_buy = self.driver.find_elements(By.CSS_SELECTOR, '.product.unlocked.enabled')

        if buildings_to_buy:
            for building in buildings_to_buy:
                building.click()  
                print(f"A building has been purchased: {building}") 
        else:
            print("No buildings available for purchase")

        return buildings_to_buy


def main():
    bot = CookieClicker()

    print(bot.open_window())
    print(bot.accept_personal_data())
    print(bot.accept_cookies())
    print(bot.set_language())

    try:
        while True:
            bot.click_cookie()
            print(bot.get_cookies_amount())
            print(bot.buy_upgrade())
            print(bot.buy_building())

    except KeyboardInterrupt:
        print(bot.close_window())


if __name__ == "__main__":
    main()
