from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CookieBot:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self.bought_buildings_count = 0

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

    def buy_item(self, item_type: str, css_selector: str, item_data: dict) -> None:  
        if item_type == "Building":
            items_to_buy = self.driver.find_elements(By.CSS_SELECTOR, css_selector)

            for name_or_id, price in item_data.items():
                for item in items_to_buy:   
                    if name_or_id in item.text:
                        item.click()
                        print(f'Purchased {item_type} {name_or_id} for {price} cakes')
                        break   
        else:
            item = self.driver.find_element(By.CSS_SELECTOR, css_selector)

            for name_or_id, price in item_data.items():
                item.click()
                print(f'Purchased {item_type} {name_or_id} for {price} cakes')   
                break

    def algorithm(self, current_money: str, upgrades: dict, buildings_info: dict, buildings_cps: dict) -> None:
        current_money = current_money.split()[0].replace(",", "")

        building_efficiency = {}
            
        for name, price in buildings_info.items():
            if name in buildings_cps:
                cps = buildings_cps[name]
                price = price.replace(",", "")
                building_efficiency[name] = int(price) / float(cps)

        sorted_items = sorted(building_efficiency.items(), key=lambda x: x[1])
        
        sorted_upgrades = sorted(upgrades.items(), key=lambda x: int(x[1]))

        if self.bought_buildings_count >= 5 and sorted_upgrades:
            upgrade_name, upgrade_price = sorted_upgrades[0]
            if int(current_money) >= int(upgrade_price):
                self.buy_item('Upgrade', f'[data-id="{upgrade_name}"]', {upgrade_name: upgrade_price})  
                self.bought_buildings_count = 0
                return
            
        if sorted_items:
            building_name, _ = sorted_items[0]
            building_price = buildings_info[building_name].replace(",", "")
            if int(current_money) >= int(building_price):
                self.buy_item('Building', '.product.unlocked.enabled', {building_name: building_price})
                self.bought_buildings_count += 1
                return


def main() -> None:
    bot = CookieBot()

    print(bot.open_window())
    print(bot.accept_personal_data())
    print(bot.accept_cookies())
    print(bot.set_language())

    try:
        while True:              
            bot.click_cookie()
            
            current_money = bot.get_cookies_amount()
            upgrades = bot.get_upgrade_info()
            buildings_info, buildings_cps = bot.get_building_info()
            bot.algorithm(current_money, upgrades, buildings_info, buildings_cps)

    except KeyboardInterrupt:
        print(bot.close_window())


if __name__ == "__main__":
    main()
