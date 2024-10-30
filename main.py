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


    def set_language(self, language_id: str = "langSelect-PL") -> str:
        select_language = self.driver.find_element(By.ID, language_id)
        select_language.click()
        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, 'bigCookie')))
        return f"Language set to {language_id}"


    def click_cookie(self) -> str:
        for _ in range(50):
            cookie = self.driver.find_element(By.ID, 'bigCookie')
            cookie.click()
        return "Cookie clicked 50 times"
    

    def close_window(self) -> str:
        self.driver.close()
        return "Window closed"


if __name__ == "__main__":
    bot = CookieClicker()
    print(bot.open_window())
    print(bot.accept_personal_data())
    print(bot.accept_cookies())
    print(bot.set_language())
    print(bot.click_cookie())
    print(bot.close_window())
