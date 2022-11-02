from django.shortcuts import render, redirect
from .models import *
import os


# Create your views here.

def home(request):
    
    if os.path.isfile("C:/Users/vkstk/OneDrive/바탕 화면/IoT_proj/iot.txt"):
        lst = []

        f = open("C:/Users/vkstk/OneDrive/바탕 화면/IoT_proj/iot.txt", 'r')

        while True:
            line_data = f.readline().strip()
            if line_data == '':
                break
            lst.append(float(line_data))

        for i in range(0, len(lst)):
            iot = Congression(num = lst[i])
            iot.save()
        
        f.close()
        os.remove("C:/Users/vkstk/OneDrive/바탕 화면/IoT_proj/iot.txt")
        
    iot_set = Congression.objects.all().order_by('-created_at')

    return render(request, 'home.html', {'iot_set':iot_set})

def delete(request):
    Congression.objects.all().delete()

    if os.path.isfile("C:/Users/vkstk/OneDrive/바탕 화면/IoT_proj/iot.txt"):
        os.remove("C:/Users/vkstk/OneDrive/바탕 화면/IoT_proj/iot.txt")

    return redirect('home')