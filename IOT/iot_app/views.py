from django.shortcuts import render, redirect
from .models import *
import os


# Create your views here.

def home(request):
    
    if os.path.isfile("iot.csv"):
        lst = []
        t = []

        f = open("iot.csv", 'r')

        while True:
            line_data = f.readline().strip()
            if line_data == '':
                break
            info = line_data.split(',')
            t.append(info[0])
            lst.append(float(info[1]))

        #for i in range(0, len(lst)):
            # iot = Congression(num = lst[i], created_at = t[i])
            # iot.save()
            
        iot = Congression(num = lst[-1], created_at = t[-1])
        iot.save()
        
        
        f.close()
        os.remove("iot.csv")
        
    iot_first = Congression.objects.all().order_by('-created_at').first()

    return render(request, 'home.html', {'iot_first':iot_first})

def delete(request):
    Congression.objects.all().delete()

    if os.path.isfile("iot.csv"):
        os.remove("iot.csv")

    return redirect('home')