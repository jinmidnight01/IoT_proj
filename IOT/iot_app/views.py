from django.shortcuts import render, redirect, get_object_or_404
from .models import *
import os

# Create your views here.

def home(request):
    return render(request, 'home.html')

def congression(request):

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
                    
        iot = Congression(num = lst[-1], created_at = t[-1])
        iot.save()
        
        
        f.close()
        os.remove("iot.csv")
        
    iot_first = Congression.objects.all().order_by('-created_at').first()
    Eat.objects.create(eat_count=0).save()
    eat_first = Eat.objects.all().first()
    Eat.objects.all().delete()
    Eat.objects.create(eat_count=eat_first.eat_count).save()
    
    return render(request, 'congression.html', {'iot_first':iot_first, 'eat_first':eat_first})

def delete(request):
    Congression.objects.all().delete()

    if os.path.isfile("iot.csv"):
        os.remove("iot.csv")

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

    
    