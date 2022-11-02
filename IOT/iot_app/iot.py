import modi
import time

# MODI 모듈의 번들을 연결하기 위해, MODI 객체를 인스턴스화합니다.
bundle = modi.MODI()
# 'ultrasonic'라는 변수에 모듈 객체를 저장합니다.
ultrasonic = bundle.ultrasonics[0]
my_list=[]
# 대상과의 거리를 측정한 값을 0 ~ 100 사이로 환산하여 반환합니다.
while True:
    ultrasonic_distance = ultrasonic.distance
    my_list.append(ultrasonic_distance)
    print(my_list)
    time.sleep(1)
    

        
    





