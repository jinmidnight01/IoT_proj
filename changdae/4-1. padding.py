import pickle

COUNT = 20
data_bundle = []
raw_data = []
padded_data = []
file = 'C:/Users/Pearl/Desktop/IoT/Codes/jinju/rnn/data.pkl'

with open(file, 'rb') as f:
    received_data = pickle.load(f)

# x_data를 raw data 로 집어넣음
for i in received_data : 
    for j in i :
        data_bundle.append(j)
        print(j)
    print()
    raw_data.append(data_bundle)
    data_bundle = []

# raw data 에서 하나씩 꺼내서
for group in raw_data : 
    # 처음, 끝, 최솟값 저장
    first_value = group[0]
    last_value = group[-1]
    min_value = min(group)

    turn_flag = 0
    
    dec_count = 0
    inc_count = 0
    total_count = 1
    
# group 예시
# turn flag                        1    
# 0         0      0      0      0      0      0      0      0    0    0     0     0    0       0    1     1     1     1     1     1     1     1     1     1     1
# [125.0, 125.0, 117.0, 117.0, 106.0, 106.0, 106.0, 99.0, 99.0, 99.0, 89.0, 89.0, 78.0, 78.0, 78.0, 69.0, 69.0, 73.0, 73.0, 73.0, 88.0, 88.0, 97.0, 97.0, 97.0, 116.0]
# turn flag가 min값에서 1로 바뀌면 이후 1로 고정된다
    for data in group : 
        if data == min_value : 
            turn_flag = 1
            # turn_flag 1 전 까지 숫자세기
        elif turn_flag ==  0 :
            dec_count += 1
            # turn_flag 1 이후 ~ 끝까지 숫자세기
        elif turn_flag == 1:
            inc_count += 1
    # 위에서 inc_count는 9개, dec_count는 15개 (total count는 1에 더하는 거라서 25)
    total_count += inc_count + dec_count
    
    if total_count == 1 :
        for i in range(COUNT):
            data_bundle.append(min_value)
    else:
        total_count -= 1

    '''
    함수만드는 알고리즘
    예시
135 60 124 일 때
23개 34개

50개

50*24/(23+34)개를 세어준다
50*34/(23+34)개를 세어준다
    '''


    # COUNT는 최대 길이수 여기선 20
    inc_iter = round(COUNT*inc_count/(total_count))
    for i in range(inc_iter) :
        data_bundle.append(round(first_value - (first_value-min_value)*i/COUNT))
    dec_iter = round(COUNT*dec_count/(total_count))
    for i in range(dec_iter) :
        data_bundle.append(round(min_value + (last_value-min_value)*i/COUNT))
    
    padded_data.append(data_bundle)
    data_bundle = []

for i in padded_data : 
    for j in i : 
        print(j)
    print()
    
import pandas as pd
df = pd.DataFrame(padded_data)
df.to_csv('tempddd.csv')