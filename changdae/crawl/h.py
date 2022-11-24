from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# fake_useragent import 하기
from fake_useragent import UserAgent

# 가짜 agent 사용
ua = UserAgent(verify_ssl=False)
UserAgent = ua.random

# 옵션 설정 - 창 최소화, agent 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=0,0")

# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument(f'user-agent={UserAgent}')
# chrome_options.add_argument('headless')

url = 'https://www.yonsei.ac.kr/_custom/yonsei/m/menu.jsp'

driver = webdriver.Chrome("changdae\crawl\chromedriver.exe", chrome_options=chrome_options)

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