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

    return render(request, 'congression.html', {'iot_first':iot_first})

def delete(request):
    Congression.objects.all().delete()

    if os.path.isfile("iot.csv"):
        os.remove("iot.csv")

    return redirect('congression')

def kaist(request):
    return render(request, 'kaist.html')

def seoul(request):
    return render(request, 'seoul.html')

def like(request):
    if request.user not in User.objects.all():
        person = User.objects.create(name=request.user)
        person.save()

    if request.user in person.follower.all():
        person.follower.remove(request.user)
        person.save()
    else:
        person.follower.add(request.user)
        person.save()
    return redirect('mypage', user_id)
    if request.user in like_b.like.all():
        like_b.like.remove(request.user)
        like_b.like_count -= 1
        like_b.save()
    else:
        like_b.like.add(request.user)
        like_b.like_count += 1
        like_b.save()
    return redirect('detail', community_id)
