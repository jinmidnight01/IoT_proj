import modi
import time
import datetime

my_list = []

# MODI 모듈의 번들을 연결하기 위해, MODI 객체를 인스턴스화합니다.
bundle = modi.MODI()
# 'ultrasonic'라는 변수에 모듈 객체를 저장합니다.
ultrasonic = bundle.ultrasonics[0]


# 대상과의 거리를 측정한 값을 0 ~ 100 사이로 환산하여 반환합니다.
while True:
    f = open("IOT/iot.csv", 'a')
    ultrasonic_distance = str(ultrasonic.distance)
    now = str(datetime.datetime.now())
    f.write(now + ',' + ultrasonic_distance + "\n")
    f.close()
    time.sleep(1)
    

        
    





