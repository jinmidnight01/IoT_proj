import modi
import time
import pickle
import matplotlib.pyplot as plt

# MODI 모듈의 번들을 연결하기 위해, MODI 객체를 인스턴스화합니다.
bundle = modi.MODI()
i=0
# 'ultrasonic'라는 변수에 모듈 객체를 저장합니다.
#mic = bundle.mics[0]
my_list=[]
ultrasonic = bundle.ultrasonics[0]
i=0
num = 0
# 대상과의 거리를 측정한 값을 0 ~ 100 사이로 환산하여 반환합니다.
while 1:
    
    
    
    ultrasonic_distance = ultrasonic.distance
    print('ultrasonic_distance:', ultrasonic_distance)
        
    #mic_volume = mic.volume
    #print('mic_volume:', mic_volume)
    
    my_list.append(tuple(ultrasonic_distance))
    

    #print(my_list)
#plt.plot(my_list)
#plt.show()

###발표 주제