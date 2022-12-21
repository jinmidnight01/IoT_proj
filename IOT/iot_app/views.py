from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


def home(request):
    return render(request, 'home.html')

def congression(request):

    # 실시간 혼잡도
    if os.path.isfile("../iot.csv"):
        lst = []
        t = []

        f = open("../iot.csv", 'r')

        while True:
            line_data = f.readline().strip()
            if line_data == '':
                break
            info = line_data.split(',')
            t.append(info[0])
            lst.append(float(info[1]))
        
        try:            
            iot = Congression(num = lst[-1], created_at = t[-1])
            iot.save()
        except:
            iot = Congression(num = 0, created_at = str(datetime.datetime.now()))
            iot.save()

        f.close()
        os.remove("../iot.csv")
        
    # 메뉴 크롤링
    if Menu.objects.filter(created_at=datetime.date.today()).count() > 0:
        url = ""
    else:
        try:
            url = 'https://www.yonsei.ac.kr/_custom/yonsei/m/menu.jsp'

            # 옵션 설정
            options = FirefoxOptions()
            options.headless = True

            # 셀레니움 업데이트 해야 함 (pip install -U selenium)
            driver = webdriver.Firefox(options=options, executable_path=r".\geckodriver.exe")

            driver.get(url)
            driver.implicitly_wait(3)

            driver.find_element(By.XPATH, '/html/body/div/div[2]/ul/li[2]/a/div/strong').click()

            # # 클릭해주고 1초 멈추기
            # time.sleep(1)

            lunchmenu = driver.find_element(By.XPATH, '/html/body/div/div[2]/ul/li[2]/div[2]/div[2]/ul/li/span[1]').text
            dinnermenu = driver.find_element(By.XPATH, '/html/body/div/div[2]/ul/li[2]/div[2]/div[3]/ul/li/span[1]').text
            time = datetime.date.today()

            a = Menu.objects.create(lunch=lunchmenu, dinner=dinnermenu, created_at=time)
            a.save()
        except:
            pass
    
    # 그래프
    x = []
    y = []
    
    if os.path.isfile("../result.csv"):
        with open(r"../result.csv",'r') as csvfile:
            plots = csv.reader(csvfile, delimiter = ',')
            sum = 0
            for row in plots:
                
                if row[1][2:-2]=='Exit' :
                    sum -= 1
                elif row[1][2:-2]=='Enter':
                    sum += 1
                x.append(row[0][-16:21])
                if sum >= 0:
                    y.append(sum)
                else: 
                    y.append(0)
                    sum = 0
        
        fig, ax = plt.subplots()
        ax.plot(x, y, linewidth = 5, label="Congression", color="#A278F4")
        
        plt.xlabel('')
        plt.ylabel('')

        plt.xticks(x, fontsize=40, rotation=45)
        plt.yticks(y, fontsize=40)
        # ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        if datetime.datetime.now().day < 10:
            day = "0"+str(datetime.datetime.now().day)
        else:
            day = str(datetime.datetime.now().day)
        plt.title(str(datetime.datetime.now().year)+'/'+str(datetime.datetime.now().month)+'/'+day, fontsize=90, fontname="Inter", fontweight="bold")

        ax.legend(fontsize=44)
        # plt.show()
        plt.rcParams["figure.figsize"] = [16,20]
        plt.savefig('static/'+str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day)+'.png')

    # 객체 생성
    iot_first = Congression.objects.all().order_by('-created_at').first()
    Eat.objects.create(eat_count=0).save()
    eat_first = Eat.objects.all().first()
    Eat.objects.all().delete()
    Eat.objects.create(eat_count=eat_first.eat_count).save()
    today_menu = Menu.objects.all().last()

    if (datetime.datetime.today().weekday() < 5):
        return render(request, 'congression.html', {'iot_first':iot_first, 'eat_first':eat_first, 'today_menu':today_menu})
    else:
        return render(request, 'congression.html', {'iot_first':iot_first, 'eat_first':eat_first})
    
def delete(request):
    Congression.objects.all().delete()

    if os.path.isfile("../iot.csv"):
        os.remove("../iot.csv")

    return redirect('congression')

def kaist(request):
    return render(request, 'kaist.html')

def seoul(request):
    return render(request, 'seoul.html')

def eat_plus(request):    
    first = Eat.objects.all().first()
    first.eat_count += 1
    first.flag = False
    first.save()
    return redirect('congression')

def eat_minus(request): 
    first = Eat.objects.all().first()
    first.eat_count -= 1
    first.flag = True
    first.save()
    return redirect('congression')

    
    