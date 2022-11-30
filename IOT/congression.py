import time
import modi
import datetime
import matplotlib.pyplot as plt

# MODI 모듈의 번들을 연결하기 위해, MODI 객체를 인스턴스화합니다.
bundle = modi.MODI()
a=[]
ultrasonic = bundle.ultrasonics[0]
num_sign=0
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

prev = datetime.datetime.now()

while True:
    time.sleep(0.05)
    ultrasonic_distance = ultrasonic.distance
    a.append(ultrasonic_distance)
    i+=1
    if num_sign<0:
        num_sign=0

    print(num_sign)
    if i<30:
        continue
    
    # distance.csv 파일 생성
    f2 = open("distance.csv", 'a')
    now = datetime.datetime.now()
    f2.write(str(now) + ',' + str(ultrasonic_distance)  + "\n")
    f2.close()

    # iot.csv 파일 생성
    f1 = open("iot.csv", 'a')
    f1.write(str(now) + ',' + str(num_sign)  + "\n")
    f1.close()
    
    # 실시간 알고리즘
    if abs(a[i-1]-a[i])>=2:
        break_count=0
        if big_gradient1<a[i]-a[i-1]:
            big_gradient5=big_gradient4
            big_gradient4=big_gradient3
            big_gradient3=big_gradient2
            big_gradient2=big_gradient1
            big_gradient1=a[i]-a[i-1]
        else:
            if big_gradient2<a[i]-a[i-1]:
                big_gradient5=big_gradient4
                big_gradient4=big_gradient3
                big_gradient3=big_gradient2
                big_gradient2=a[i]-a[i-1]
            elif big_gradient3<a[i]-a[i-1]:
                big_gradient5=big_gradient4
                big_gradient4=big_gradient3
                big_gradient3=a[i]-a[i-1]
            elif big_gradient4<a[i]-a[i-1]:
                big_gradient5=big_gradient4
                big_gradient4=a[i]-a[i-1]
            elif big_gradient5<a[i]-a[i-1]:
                big_gradient5=a[i]-a[i-1]

        if small_gradient1>a[i]-a[i-1]:
            small_gradient5=small_gradient4
            small_gradient4=small_gradient3
            small_gradient3=small_gradient2
            small_gradient2=small_gradient1
            small_gradient1=a[i]-a[i-1]
        else:
            if small_gradient2>a[i]-a[i-1]:
                small_gradient5=small_gradient4
                small_gradient4=small_gradient3
                small_gradient3=small_gradient2
                small_gradient2=a[i]-a[i-1]
            elif small_gradient3>a[i]-a[i-1]:
                small_gradient5=small_gradient4
                small_gradient4=small_gradient3
                small_gradient3=a[i]-a[i-1]
            elif small_gradient4>a[i]-a[i-1]:
                small_gradient5=small_gradient4
                small_gradient4=a[i]-a[i-1]
            elif small_gradient5>a[i]-a[i-1]:
                small_gradient5=a[i]-a[i-1]


    if abs(a[i-1]-a[i])<2:
        break_count+=1

    if break_count>7:
        break_count=0
        if small_gradient2==0 or big_gradient2==0:
            small_gradient2=0
            big_gradient2=0
        if small_gradient3==0 or big_gradient3==0:
            small_gradient3=0
            big_gradient3=0
        if small_gradient4==0 or big_gradient4==0:
            small_gradient4=0
            big_gradient4=0
        if small_gradient5==0 or big_gradient5==0:
            small_gradient5=0
            big_gradient5=0

        if abs(big_gradient1+big_gradient2+big_gradient3+0.95*big_gradient4+0.95*big_gradient5)/5>abs(small_gradient1+small_gradient2+small_gradient3+0.95*small_gradient4+0.95*small_gradient5)/5:
            num_sign+=1
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
            
        elif abs(big_gradient1+big_gradient2+big_gradient3+0.95*big_gradient4+0.95*big_gradient5)/5<abs(small_gradient1+small_gradient2+small_gradient3+0.95*small_gradient4+0.95*small_gradient5)/5:
            num_sign-=1
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
            
        else:
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