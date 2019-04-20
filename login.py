from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
import pickle

driver = webdriver.Chrome()
driver.get('https://www.facebook.com')

username = driver.find_element_by_xpath('//*[@id="email"]')
username.send_keys("")

password = driver.find_element_by_xpath('//*[@id="pass"]')
password.send_keys("")

login = driver.find_element_by_xpath('//*[@id="u_0_2"]')
login.click()

time.sleep(15)

pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
