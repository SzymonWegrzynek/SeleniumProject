from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading


class CookieBot:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()

    def open_window(self) -> str:
        self.driver.get('https://orteil.dashnet.org/cookieclicker/')
        self.driver.maximize_window()
        return "Window opened and maximized"
    
    def close_window(self) -> str:
        self.driver.close()
        return "Window closed"
    
    def accept_personal_data(self) -> str:
        personal_data_confirm = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'fc-button-label'))) 
        personal_data_confirm.click()
        return "Personal data accepted"

    def accept_cookies(self) -> str:
        accept_cookies = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'cc_btn_accept_all')))
        accept_cookies.click()
        return "Cookies accepted"

    def set_language(self) -> str:
        select_language = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'langSelect-EN')))
        select_language.click()
        return "Set language"

    def click_cookie(self) -> None:
        cookie = self.driver.find_element(By.ID, 'bigCookie')
        cookie.click() 

    def get_cookies_amount(self) -> str:
        cookie_amount = self.driver.find_element(By.ID, 'cookies').text
        return cookie_amount

    def get_upgrade_info(self) -> list:
        upgrades_info = {}

        upgrades_cps_data = self.driver.execute_script("""
        const upgradesData = {};
        Object.values(Game.UpgradesInStore).forEach(upgrade => {
            upgradesData[upgrade.id] = upgrade.basePrice;

        });
        return upgradesData;
        """)

        for upgrade_name, upgrade_data in upgrades_cps_data.items():
            if upgrade_name not in upgrades_info:
                upgrades_info[upgrade_name] = upgrade_data

        return upgrades_info
        
    def get_building_info(self) -> dict:
        buildings_info = {}
        buildings_cps = {}

        buildings_to_buy = self.driver.find_elements(By.CSS_SELECTOR, '.product.unlocked.enabled')
        disabled_buildings_to_buy = self.driver.find_elements(By.CSS_SELECTOR, '.product.unlocked.disabled')

        if buildings_to_buy:
            for building in buildings_to_buy:
                name = building.find_element(By.CSS_SELECTOR, '.title.productName').text
                price = building.find_element(By.CSS_SELECTOR, '.price').text
                buildings_info[name] = price

        if disabled_buildings_to_buy:
            for building in disabled_buildings_to_buy:
                name = building.find_element(By.CSS_SELECTOR, '.title.productName').text
                price = building.find_element(By.CSS_SELECTOR, '.price').text
                buildings_info[name] = price

        buildings_cps_data = self.driver.execute_script("""
        const cpsData = {};
        Object.values(Game.ObjectsById).forEach(building => {
            cpsData[building.name] = building.storedCps;
        });
        return cpsData; 
        """)
        
        for name in buildings_info.keys():
            if name in buildings_cps_data:
                buildings_cps[name] = buildings_cps_data[name]

        return buildings_info, buildings_cps

    def buy_item(self, item_type: str, css_selector: str, item_data: dict, current_amount_of_money: str) -> None:
        current_money = current_amount_of_money.split()[0]

        for name_or_id, price in item_data.items():
            if int(current_money) >= int(price):
                item_to_buy = self.driver.find_elements(By.CSS_SELECTOR, css_selector)

                for item in item_to_buy:
                    item.click()
                    print(f'Purchased {item_type} {name_or_id} for {price} cakes')
                    break
    
    def algorithm(self, current_amount_of_money: str, upgrades: dict, buildings_info: dict, buildings_cps: dict) -> dict:
        current_money = current_amount_of_money.split()[0]

        building_efficiency = {}

        for name, price in buildings_info.items():  
            if name in buildings_cps: 
                cps = buildings_cps[name] 
                price = int(price) 
                building_efficiency[name] = price / cps 

        sorted_buildings = sorted(building_efficiency.items(), key=lambda x: x[1])

        for building_name, _ in sorted_buildings:
            building_price = buildings_info.get(building_name)

            if int(current_money) >= int(building_price):
                self.buy_item('building', '.product.unlocked.enabled', {building_name: building_price}, current_money)
                break 

        for upgrade_name, upgrade_price in upgrades.items():
            if int(current_money) >= int(upgrade_price):
                self.buy_item('upgrade', '.crate.upgrade.enabled', {upgrade_name: upgrade_price}, current_money)
                break

        return sorted_buildings  


def main() -> None:
    bot = CookieBot()

    print('\n' + '=' * 40)
    print(bot.open_window())
    print(bot.accept_personal_data())
    print(bot.accept_cookies())
    print(bot.set_language())
    print('=' * 40 + '\n')

    try:
        while True:              
            click_thread = threading.Thread(target=bot.click_cookie)
            click_thread.daemon = True  
            click_thread.start()
            
            current_amount_of_money = bot.get_cookies_amount()
            upgrades = bot.get_upgrade_info()
            buildings_info, buildings_cps = bot.get_building_info()
            algorithm = bot.algorithm(current_amount_of_money, upgrades, buildings_info, buildings_cps)

            print('\n' + '=' * 40)
            print(f'current amount of money: {current_amount_of_money}')
            print('-' * 40)
            print(f'upgrades: {upgrades}')
            print('-' * 40)
            print(f'buildings info: {buildings_info}')
            print(f'buildings cps: {buildings_cps}')
            print('-' * 40)
            print(f'algorithm: {algorithm}')
            print('=' * 40 + '\n')
    
    except KeyboardInterrupt:
        print(bot.close_window())


if __name__ == "__main__":
    main()
