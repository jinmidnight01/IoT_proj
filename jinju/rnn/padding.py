import pickle

COUNT = 20
data_bundle = []
raw_data = []
padded_data = []
file = 'C:/Users/Pearl/Desktop/IoT/Codes/jinju/rnn/data.pkl'

with open(file, 'rb') as f:
    received_data = pickle.load(f)

for i in received_data : 
    for j in i :
        data_bundle.append(j)
        print(j)
    print()
    raw_data.append(data_bundle)
    data_bundle = []

for group in raw_data : 
    first_value = group[0]
    last_value = group[-1]
    min_value = min(group)

    turn_flag = 0
    
    dec_count = 0
    inc_count = 0
    total_count = 1
    
    for data in group : 
        if data == min_value : 
            turn_flag = 1
        elif turn_flag ==  0 :
            dec_count += 1
        elif turn_flag == 1:
            inc_count += 1
    total_count += inc_count + dec_count
    
    if total_count != 1 :
        total_count -= 1
    
    inc_iter = round(COUNT*inc_count/(total_count))
    for i in range(inc_iter) :
        data_bundle.append(round(first_value - abs(first_value-min_value)*i*inc_count/(total_count)))
    dec_iter = round(COUNT*dec_count/(total_count))
    for i in range(dec_iter) :
        data_bundle.append(round(min_value + abs(last_value-min_value)*i*dec_count/(total_count)))
    
    padded_data.append(data_bundle)
    data_bundle = []

for i in padded_data : 
    for j in i : 
        print(j)
    print()