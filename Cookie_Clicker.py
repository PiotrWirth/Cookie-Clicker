from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)

service = Service("C:\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(options=options,service=service)
 
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, 'cookie')

items = driver.find_elements(By.CSS_SELECTOR,'#store div')
items_ids = [ item.get_attribute('id') for item in items]


timeout = time.time() + 60*5
timecheck = time.time() + 5



while True:

    cookie.click()

    if time.time() > timecheck:    
        
        #Get all upgrade <b> tags and convert them into integers
        price = driver.find_elements(By.CSS_SELECTOR, "#store b")
        prices = [int(element.text.split('-')[1].strip().replace(",","")) for element in price if element.text != ""]
        
        #Create dictionary of store items and price  
        cookie_upgrades = {prices[n]:items_ids[n] for n in range(len(prices))}

        #Get current cookie count
        cookie_money = int(driver.find_element(By.ID, 'money').text.replace(",", ""))

        #Find affordable upgrades
        purchasable_items = {cost:id for (cost,id) in cookie_upgrades.items() if cookie_money > cost}

        #Purchase the most expensive affordable upgrade
        highest_purchasable_items = max(purchasable_items)
        to_purchase_id = purchasable_items[highest_purchasable_items]

        driver.find_element(By.ID, to_purchase_id).click()

        timecheck = time.time() + 5
    
    if time.time() > timeout:
        cookie_per_s = driver.find_element(By.ID, 'cps').text
        print(cookie_per_s)
        break
