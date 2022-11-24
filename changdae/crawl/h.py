from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve
import os

url = 'https://www.yonsei.ac.kr/_custom/yonsei/m/menu.jsp'

driver = webdriver.Chrome("changdae\crawl\chromedriver.exe")
driver.get(url)
driver.implicitly_wait(3)

driver.find_element(By.XPATH, '/html/body/div/div[2]/ul/li[2]/a/div/strong').click()

# 클릭해주고 1초 멈추기
time.sleep(1)

lunch = driver.find_element(By.XPATH, '/html/body/div/div[2]/ul/li[2]/div[2]/div[2]/ul/li/span[1]').text
dinner = driver.find_element(By.XPATH, '/html/body/div/div[2]/ul/li[2]/div[2]/div[3]/ul/li/span[1]').text

print('점심은' , lunch)
print('저녁은' , dinner)

driver.quit()