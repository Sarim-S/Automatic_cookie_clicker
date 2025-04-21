from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

cookie_url = "https://orteil.dashnet.org/experiments/cookie/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver  = webdriver.Chrome(options=chrome_options)
driver.get(url=cookie_url)

cookie = driver.find_element(By.ID, value="cookie")

items = driver.find_elements(By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 7
game_timer = time.time() + 60*1

while True:
    
    cookie.click()

    if time.time() > timeout:

        all_items = driver.find_elements(By.CSS_SELECTOR, value="#store b")
        item_prices = []

        for item in all_items:
            if item.text != "":
                number = item.text.split(" - ")[1]
                price = number.replace(",", "")
                item_prices.append(int(price))
        

        upgrade_info = {}
        for n in range(len(item_prices)):
            upgrade_info[item_prices[n]] = item_ids[n]
        
        current_cookies = driver.find_element(By.ID, value="money").text
        if "," in current_cookies:
            current_cookies = current_cookies.replace(",", "")
        cookie_amount = int(current_cookies)

        affordable = {}
        for cost, upgrade in upgrade_info.items():
            if cookie_amount > cost:
                affordable[cost] = upgrade

        greatest_upgrade = max(affordable)
        upgrade_to_buy = affordable[greatest_upgrade]

        driver.find_element(By.ID, value=upgrade_to_buy).click()
        
        timeout = time.time() + 5
    
    if time.time() > game_timer:
        clicks_per_second = driver.find_element(By.ID, value="cps").text
        print(f"Score was: {clicks_per_second}")
        break

driver.quit()


