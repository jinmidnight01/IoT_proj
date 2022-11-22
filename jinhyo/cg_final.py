import time
import modi
import datetime
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pytz import timezone

# 구글 스프레드시트 연동
json_key_path = "./jinhyo/modi-369003-634526ec889a.json"
gc = gspread.service_account(filename=json_key_path)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1WCdOrjh1FzOp5NaOAqamWx5uwQkF_L4evwcDBUQUCGI/edit#gid=0'
doc = gc.open_by_url(spreadsheet_url)
sheet1 = doc.worksheet("sheet1")

# MODI 모듈의 번들을 연결하기 위해, MODI 객체를 인스턴스화합니다.
#bundle = modi.MODI()
a=[]
#ultrasonic = bundle.ultrasonics[0]
num_sign=1
big_gradient1=0
big_gradient2=0
big_gradient3=0
big_gradient4=0
big_gradient5=0
small_gradient1=0
small_gradient2=0
small_gradient3=0
small_gradient4=0
small_gradient5=0
break_count=0
i=-1
data = []

# 스프레드시트 작성
while True:
    time.sleep(0.05)
    #ultrasonic_distance = ultrasonic.distance
    #a.append(ultrasonic_distance)
    i+=1
    if num_sign<0:
        num_sign=0

    print(num_sign)
    if i<30:
        continue
    
    # 파일 생성
    f = open("IOT/iot.csv", 'a')
    now = str(datetime.datetime.now(timezone('Asia/Seoul')))
    f.write(now + ',' + str(num_sign)  + "\n")
    f.close()

