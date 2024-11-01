from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WikiData:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()

    def open_window(self) -> str:
        self.driver.get('https://cookieclicker.fandom.com/wiki/Upgrades')
        self.driver.maximize_window()
        return "Wiki opened and maximized"
    
    def close_window(self) -> str:
        self.driver.close()
        return "Wiki closed"

    def accept_cookies(self) -> str:
        accept_cookies = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-tracking-opt-in-accept="true"]')))
        accept_cookies.click()
        return "Cookies accepted - Wiki"

    def get_wiki_upgrade_data(self, ids: list) -> dict:
        wiki_upgrade_data = {}

        tr_element = self.driver.find_elements(By.CSS_SELECTOR, 'tr')

        for id in ids:
            for find_id in tr_element:
                td_element = find_id.find_elements(By.TAG_NAME, 'td')

                if td_element:
                    row_id = td_element[-1].text.strip()

                if row_id == str(id):
                    price = find_id.find_element(By.CSS_SELECTOR, 'td[data-sort-value="1E2"]').text
                    wiki_upgrade_data[id] = price
                    break
        
        return wiki_upgrade_data


class CookieClicker:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()

    def open_window(self) -> str:
        self.driver.get('https://orteil.dashnet.org/cookieclicker/')
        self.driver.maximize_window()
        return "Game opened and maximized"
    
    def close_window(self) -> str:
        self.driver.close()
        return "Game closed"
    
    def accept_personal_data(self) -> str:
        personal_data_confirm = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, 'fc-button-label'))) 
        personal_data_confirm.click()
        return "Personal data accepted - Game"

    def accept_cookies(self) -> str:
        accept_cookies = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, 'cc_btn_accept_all')))
        accept_cookies.click()
        return "Cookies accepted - Game"

    def set_language(self) -> str:
        select_language = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.ID, 'langSelect-PL')))
        select_language.click()
        return "Set language - Game"

    def click_cookie(self) -> None:
        cookie = self.driver.find_element(By.ID, 'bigCookie')
        cookie.click()

    def get_cookies_amount(self) -> str:
        cookie_amount = self.driver.find_element(By.ID, 'cookies').text
        return cookie_amount

    def get_upgrade_info(self) -> list:
        upgrades_id = []

        upgrades_to_buy = self.driver.find_elements(By.CSS_SELECTOR, '.crate.upgrade.enabled')

        if upgrades_to_buy:
            for upgrade in upgrades_to_buy:
                id = upgrade.get_attribute('data-id')
                upgrades_id.append(id)
        else:
            print("No upgrades available for purchase")

        return upgrades_id

    def buy_upgrade(self, upgrades_data: dict, current_amount_of_money: str) -> None:
        current_money = current_amount_of_money.split()[0]

        for id, price in upgrades_data.items():
            if current_money >= price:
                upgrades_to_buy = self.driver.find_elements(By.CSS_SELECTOR, '.crate.upgrade.enabled')

                for upgrade in upgrades_to_buy:
                    upgrade.click()
                    print(f'Purchased upgrade {id} for {price} cakes')
                    break
        
    def get_building_info(self) -> dict:
        buildings_info = {}

        buildings_to_buy = self.driver.find_elements(By.CSS_SELECTOR, '.product.unlocked.enabled')

        if buildings_to_buy:
            for building in buildings_to_buy:
                name = building.find_element(By.CSS_SELECTOR, '.title.productName').text
                price = building.find_element(By.CSS_SELECTOR, '.price').text
                buildings_info[name] = price
        else:
            print("No buildings available for purchase")

        return buildings_info
    
    def buy_building(self, buildings_data: dict, current_amount_of_money: str) -> None:
        current_money = current_amount_of_money.split()[0]

        for name, price in buildings_data.items():
            if current_money >= price:
                buildings_to_buy = self.driver.find_elements(By.CSS_SELECTOR, '.product.unlocked.enabled')

                for building in buildings_to_buy:
                    building.click()
                    print(f'Purchased building {name} for {price} cakes')
                    break

def main() -> None:
    bot = CookieClicker()
    wiki = WikiData()

    print(wiki.open_window())
    print(wiki.accept_cookies())

    print(bot.open_window())
    print(bot.accept_personal_data())
    print(bot.accept_cookies())
    print(bot.set_language())

    try:
        while True:
            bot.click_cookie()

            current_amount_of_money = bot.get_cookies_amount()
            print(current_amount_of_money)

            upgrades_ids = bot.get_upgrade_info()
            print(upgrades_ids)

            buildings_data = bot.get_building_info()
            print(buildings_data)

            upgrades_data = wiki.get_wiki_upgrade_data(upgrades_ids)
            print(upgrades_data)
            
            bot.buy_upgrade(upgrades_data, current_amount_of_money)
            bot.buy_building(buildings_data, current_amount_of_money)
    
    except KeyboardInterrupt:
        print(bot.close_window())
        print(wiki.close_window())


if __name__ == "__main__":
    main()
