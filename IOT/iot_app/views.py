from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
import datetime
import matplotlib.pyplot as plt
<<<<<<< HEAD
<<<<<<< HEAD
import matplotlib.ticker as mtick
=======
import csv
# from .refine_final import Mentos
import numpy as np
import matplotlib.ticker as mticker  

# # 그래프 추출
# data = Mentos()

# # 1. total data graph
# x = []
# y = []

# with open(r"C:\Users\vkstk\OneDrive\바탕 화면\IoT_proj\IOT\distance.csv",'r') as csvfile:
#     plots = csv.reader(csvfile, delimiter = ',')
    
#     for row in plots:
#         x.append(row[0])
#         y.append(float(row[1]))

# data.abstract()

# # 2. abstracted data graph
# x = []
# y = []
# n=0

# for group in data.abstracted_data :
#     for date_distance in group:
#         x.append(date_distance[0])
#         y.append(float(date_distance[1]))
#     for i in range(3): # to check the group
#         x.append(str(n))
#         y.append(0)
#         n += 1
        
# data.merge()

# # 3. merged data graph
# x = []
# y = []

# for group in data.abstracted_data :
#     for date_distance in group:
#         x.append(date_distance[0])
#         y.append(float(date_distance[1]))
        
# data.trim()

# # 4. trimmed data graph
# x = []
# y = []
# n = 0

# for group in data.trimmed_data :
#     for date_distance in group:
#         x.append(date_distance[0])
#         y.append(float(date_distance[1]))
#         # print(date_distance)
#     for i in range(3): # to check the group
#         x.append(str(n))
#         y.append(0)
#         n += 1
#     # print()
    
# data.inout()

>>>>>>> parent of 8a317cd (구현 모두 완료)
=======
import matplotlib.ticker as mtick
>>>>>>> 6a2eedb5284d90d7a23c92cb6da17ca0d4c83bf4


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
    
    # # 그래프
    # if os.path.isfile("result.csv"):
    #     os.remove("result.csv")   
    
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 6a2eedb5284d90d7a23c92cb6da17ca0d4c83bf4
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
<<<<<<< HEAD
=======
    # for i in data.analyzed_data:
    #     print(i)
    
    # f2 = open("result.csv", 'w')
    # for i in data.analyzed_data:
    #     f2.write(str(i)+'\n')
    # f2.close()
    
    # x = []
    # y = []
    
    # with open(r'C:\Users\vkstk\OneDrive\바탕 화면\IoT_proj\IOT\result.csv','r') as csvfile:
    #     plots = csv.reader(csvfile, delimiter = ',')
    #     sum = 0
    #     for row in plots:
            
    #         if row[1][2:-2]=='Exit' :
    #             sum -= 1
    #         elif row[1][2:-2]=='Enter':
    #             sum += 1
            
    #         # print(row[1][1:-1])
    #         x.append(row[0][-16:21])
    #         if (sum >=0 ):
    #             y.append(sum)
    #         else:
    #             sum = 0
    
    # fig, ax = plt.subplots()
    # ax.plot(x, y, linewidth = 0.72)
    # plt.xlabel('Time')
    # plt.ylabel('Congression')
    # plt.xticks(x)
    # plt.yticks(y)
    # # plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter("%i"))
    # # plt.title(str(datetime.datetime.now().year)+"/"+str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day))
    # plt.savefig('static/{name}.png'.format(name=str(datetime.datetime.now().month) + "_" + str(datetime.datetime.now().day)))
>>>>>>> parent of 8a317cd (구현 모두 완료)
=======
>>>>>>> 6a2eedb5284d90d7a23c92cb6da17ca0d4c83bf4

    # 객체 생성
    iot_first = Congression.objects.all().order_by('-created_at').first()
    Eat.objects.create(eat_count=0).save()
    eat_first = Eat.objects.all().first()
    Eat.objects.all().delete()
    Eat.objects.create(eat_count=eat_first.eat_count).save()
<<<<<<< HEAD
    today_menu = Menu.objects.all().first()
=======
    today_menu = Menu.objects.all().last()
>>>>>>> 6a2eedb5284d90d7a23c92cb6da17ca0d4c83bf4

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

    
    