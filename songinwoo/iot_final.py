import time
import pickle
import modi
#import matplotlib.pyplot as plt

# MODI 모듈의 번들을 연결하기 위해, MODI 객체를 인스턴스화합니다.
bundle = modi.MODI()
a=[]
ultrasonic = bundle.ultrasonics[0]
num_inout=[]
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

while 1:
    time.sleep(0.05)
    ultrasonic_distance = ultrasonic.distance
    print('ultrasonic_distance:', ultrasonic_distance)
    a.append(ultrasonic_distance)
    i+=1
    print(num_sign)
    if i<30:
        num_inout.append(num_sign)
        continue

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

    #print(big_gradient1, big_gradient2,big_gradient3,big_gradient4,big_gradient5,
    #      small_gradient1, small_gradient2,small_gradient3,small_gradient4,small_gradient5 ,num_sign)
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
            #print(abs(big_gradient1+big_gradient2+big_gradient3+0.95*big_gradient4+0.95*big_gradient5)/5,
            #      abs(small_gradient1+small_gradient2+small_gradient3+0.95*small_gradient4+0.95*small_gradient5)/5)
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
            
            for j in range(1,7):
                num_inout[i-j]=num_sign
        elif abs(big_gradient1+big_gradient2+big_gradient3+0.95*big_gradient4+0.95*big_gradient5)/5<abs(small_gradient1+small_gradient2+small_gradient3+0.95*small_gradient4+0.95*small_gradient5)/5:
            #print(abs(big_gradient1+big_gradient2+big_gradient3+0.95*big_gradient4+0.95*big_gradient5)/5,
            #      abs(small_gradient1+small_gradient2+small_gradient3+0.95*small_gradient4+0.95*small_gradient5)/5)
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
            
            for j in range(1,7):
                num_inout[i-j]=num_sign
        else:
            #print(abs(1.1*big_gradient1+big_gradient2+big_gradient3)/3,abs(1.1*small_gradient1+small_gradient2+small_gradient3)/3)
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

    num_inout.append(num_sign)
