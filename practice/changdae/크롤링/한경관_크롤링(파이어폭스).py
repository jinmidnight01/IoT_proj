from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

url = 'https://www.yonsei.ac.kr/_custom/yonsei/m/menu.jsp'

# 옵션 설정
options = FirefoxOptions()
options.headless = True

# 셀레니움 업데이트 해야 함 (pip install -U selenium)
driver = webdriver.Firefox(options=options, executable_path="changdae/crawl/geckodriver.exe")

driver.get(url)
driver.implicitly_wait(3)

driver.find_element(By.XPATH, '/html/body/div/div[2]/ul/li[2]/a/div/strong').click()

# # 클릭해주고 1초 멈추기
time.sleep(1)

lunch = driver.find_element(By.XPATH, '/html/body/div/div[2]/ul/li[2]/div[2]/div[2]/ul/li/span[1]').text
dinner = driver.find_element(By.XPATH, '/html/body/div/div[2]/ul/li[2]/div[2]/div[3]/ul/li/span[1]').text

print('점심은' , lunch)
print('저녁은' , dinner)

driver.quit()