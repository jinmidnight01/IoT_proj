from django.shortcuts import render, redirect
from .models import *
import os


# Create your views here.

def home(request):
    
    if os.path.isfile("iot.txt"):
        lst = []

        f = open("iot.txt", 'r')

        while True:
            line_data = f.readline().strip()
            if line_data == '':
                break
            lst.append(float(line_data))

        for i in range(0, len(lst)):
            iot = Congression(num = lst[i])
            iot.save()
        
        f.close()
        os.remove("iot.txt")
        
    iot_set = Congression.objects.all().order_by('-created_at')

    return render(request, 'home.html', {'iot_set':iot_set})

def delete(request):
    Congression.objects.all().delete()

    if os.path.isfile("iot.txt"):
        os.remove("iot.txt")

    return redirect('home')