import time
import pickle
import modi
import datetime
import matplotlib.pyplot as plt

bundle = modi.MODI()
ultrasonic = bundle.ultrasonics[0]

MIN_FREQ = 10
STRUCTURE_SIZE = 3 # memory size to store the data
GLITCH_ALLOWANCE = 5 # standard of rate-of-change to determine the data validity
TIME_ALLOWANCE = 0.2
STANDARD_CHANGE_ALLOWANCE = 50
RATIO = 2/3
MIN_CHANGE_ALLOWANCE = 200
REPEAT_ALLOWANCE = 3

repeat_count = 0 # to determine whether it's fixed or minimum/maximum
state = 0 # to remember the previous gradient of the graph > abstraction
prev_distance = 0
new_abstraction = False # to determine whether new group is updated
merge_flag = [] # to determine whether the group is already merged or not
min_set = [] # set of minimum values of every group
new_group = False
i = -1 # number of current abstracted_group
astate = 0 # to remember the previou gradient of the graph > inout
previous_result = 0 # to avoid writing same result

def getTimeValue(time) : # getting sum of hour/min/sec as seconds
    (h,m,s) = time.split(":")
    return int(h)*3600 + int(m)*60 + float(s)

class Mentos :
    # . . .
    # data structue to 
    # 1. abstract requisite data
    # 2. convert requisite data into intuitive form
    # . . .
    # receive data from the sensor directly
    # PROS : memory efficient // only STRUCTURE SIZE memory required
    # . . .
    mentos = [] # storage for the time-distance data
    pre_abstracted_data = []
    abstracted_data = []
    
    def standard(self):
        # . . .
        # return the fixed value of the current area
        # >> len(mentos) != 0 so it's safe to use :D
        # . . .
        distance = []
        for time_distance in self.mentos : 
            distance.append(float(time_distance[1]))
        return sum(distance)/len(distance)
            
    def enqueue(self, time_distance):
        # . . .
        # queue property of the mentos implementation
        # . . .
        self.mentos.append(time_distance)
        # dequeue the oldest data if the structure is FULL
        if len(self.mentos) > STRUCTURE_SIZE :
            self.mentos.pop(0)
     
data = Mentos()

while True : 
    f = open("result.csv", 'a')
    time.sleep(0.05)
    time_distance = (datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S.%f"),ultrasonic.distance)

    ########################ABSTRACTION#########################
    # . . .
    # abstract the essential data from the csv file which are sets of 
    # 1. current front fixed-data sample
    # 2. current essential data
    # 3. current rear fixed-data sample
    # . . .
    data.enqueue(time_distance)
    current_distance = float(data.mentos[-1][1]) 
    # if the gradient is DECREASING
    if (prev_distance - current_distance) >= GLITCH_ALLOWANCE : 
        # and the gradient had been INCREASING
        if state == 2 :
            if len(data.pre_abstracted_data)!=0:
                # this is a new group after the completed group
                # so append the completed group to the abstracted_data
                data.abstracted_data.append(data.pre_abstracted_data)
                #print(data.pre_abstracted_data,"1")
                i += 1
                merge_flag.append(False)
                new_abstraction = True
            else : 
                state = 0
            # and empty the temporary list for the new group
            data.pre_abstracted_data = []
            
        
        # mark the state as DECREASING
        state = 1
        # if the mentos is NOT full, it means the previous data was appended
        if len(data.mentos) != STRUCTURE_SIZE :
            # so just append the current data
            data.pre_abstracted_data.append(data.mentos.pop())
        else : 
            # if the mentos IS full, it means this is the first essential data
            # so append the data including
            # 1. current front fixed-data sample
            data.pre_abstracted_data.append(data.mentos.pop(-2))
            # 2. current essential data
            data.pre_abstracted_data.append(data.mentos.pop())
        
        # the value has changed so reset the count
        repeat_count = 0
        
    # if the gradient is INCREASING
    elif (prev_distance - current_distance) <= -GLITCH_ALLOWANCE:
        # if the graph's been decreasing or increasing, this is a valid value
        if state == 1 or state == 2:
            # mark the state as INCREASING
            state = 2
            # and append the current essential data
            data.pre_abstracted_data.append(data.mentos.pop())
        # the value has changed so reset the count
        repeat_count = 0
            
    # if the gradient is SIMILIAR   
    else :
        # and the graph has been increasing
        if state == 2 :
        # and the value repeated enough time to be fixed value
            if repeat_count >= MIN_FREQ:
                if len(data.pre_abstracted_data)!=10:
                    for l in range(10):
                        data.pre_abstracted_data.pop(-1)
                    # append the group to the abstracted_data
                    data.abstracted_data.append(data.pre_abstracted_data)
                    #print(data.pre_abstracted_data,"2")
                    i += 1
                    merge_flag.append(False)
                    new_abstraction = True
                    # and empty the group for the next data
                data.pre_abstracted_data = []
                # then reset the count and the state
                state = 0
                repeat_count = 0
                
                        
            # but can't determine if the value is fixed or just repeated
            else : 
                # append the data and count that data just in case
                repeat_count += 1
                data.pre_abstracted_data.append(data.mentos.pop())
                        
        # and the graph has been decreasing
        elif state == 1 : 
            # and the value repeated enough time to be fixed value
            if repeat_count >= MIN_FREQ :
                # reset the list, state and the count
                data.pre_abstracted_data = []
                state = 0
                repeat_count = 0
            # but can't determine if the value is fixed or just repeated
            else :
                # append the data and count that data just in case
                repeat_count += 1
                data.pre_abstracted_data.append(data.mentos.pop())
            
    #update the previous_distance         
    prev_distance = current_distance
    
    ##########################MERGE###########################
    # . . .
    # merge incomplete groups into the complete one
    # . . .
    if new_abstraction == True:
        new_abstraction = False # turn off the the new_abstaction alarm
        
        if i > 1:
            group = data.abstracted_data[i-1]
            min_data = min([float(j) for k,j in group])
            front_fixed_data = float(group[0][1])
            rear_fixed_data = float(group[-1][1])
            
            # if the graph seems like it didn't reach its edge nor started from the minimum
            if abs(front_fixed_data - rear_fixed_data) > STANDARD_CHANGE_ALLOWANCE :
                current_start_time = getTimeValue(group[0][0][-15:])
                current_end_time = getTimeValue(group[-1][0][-15:])
                front_time_gap = 1000
                rear_time_gap = 1000
                    
                previous_group = data.abstracted_data[i-2]
                previous_end_time = getTimeValue(previous_group[-1][0][-15:])
                front_time_gap = abs(previous_end_time - current_start_time)
                        
                next_group = data.abstracted_data[i]
                next_start_time = getTimeValue(next_group[0][0][-15:])
                rear_time_gap = abs(next_start_time - current_end_time)
    
                # if the data is closer to the previous data
                if front_time_gap < rear_time_gap and merge_flag[i-2]==False:
                    data.abstracted_data[i-2] += data.abstracted_data.pop(i-1)
                    merge_flag[i-2] = True
                    i -= 1
                    
                elif front_time_gap > rear_time_gap and merge_flag[i-1]==False:
                    data.abstracted_data[i-1] += data.abstracted_data.pop(i)
                    merge_flag[i-1] = True
                    i -= 1
                    
            # if the group graph has abnormal shape (which resembles a straw)
            elif abs(front_fixed_data - min_data) < GLITCH_ALLOWANCE:
                if merge_flag[i-2]==False:
                    data.abstracted_data[i-2] += data.abstracted_data.pop(i-1)
                    i -= 1
                    
            elif abs(rear_fixed_data - min_data) < GLITCH_ALLOWANCE:
                if merge_flag[i-1]==False:
                    data.abstracted_data[i-1] += data.abstracted_data.pop(i)
                    i -= 1
        
        ##########################TRIM###########################
        # . . .
        # trim the glitch-group
        # !!!need 2 dummy data at the last
        # . . .
        if i > 1:
            group = data.abstracted_data[i-2]
            distance = []
            min_count = 0
            
            for t,d in group:
                distance.append(float(d))
            min_set.append(min(distance))
            
            # counting the minimum-like value in the group
            for d in distance:
                if abs(d-min(distance)) < GLITCH_ALLOWANCE:
                    min_count += 1
            
            # if minimum-like value exists more than the given ratio, it's not valid  
            if min_count > len(distance)*RATIO:
                data.abstracted_data.pop(i-2)
                min_set.pop(i-2)
                i -= 1
            
            if i > 3:
                min_standard = min(min_set[i-4], min_set[i-2])
                if min_set[i-3] - min_standard > MIN_CHANGE_ALLOWANCE:
                    data.abstracted_data.pop(i-3)
                    min_set.pop(i-3)
                    i -= 1
        
        ##########################ANALYZE###########################
        if i > 1:
            astate = 0
            group = data.abstracted_data[i-2]
            min_data = min([float(j) for k,j in group])
            previous_value = float(group[0][1])
            repeat = 0

            # 1. front/rear distance value with weight of 45
            front_value = float(group[0][1])
            rear_value = float(group[-1][1])
            # 2. decreasing/increasing data number with weight of 35
            decrease_count = 0
            decrease_min = 1000
            increase_count = 0
            increase_max = 0
            # 3. value right in front/behind of the minimum value
            min_front_value =  1
            min_rear_value = 1

            # counting the decreasing/increasing data, determining front/rear min data
            for o in range(len(group)):
                distance = float(group[o][1])
                if repeat >= REPEAT_ALLOWANCE:
                    if state == 0 :
                        front_value = previous_value
                    elif state == 2:
                        rear_value = previous_value
                if distance == min_data:
                    if state == 0:
                        if float(group[o-1][1])!=front_value:
                            min_front_value = float(group[o-1][1])
                    state = 1
                elif state == 0 and (distance <= decrease_min or abs(distance-decrease_min)<=GLITCH_ALLOWANCE):
                    decrease_count += 1
                    decrease_min = distance
                    if distance == previous_value:
                        repeat += 1
                    else : 
                        repeat = 0
                elif state > 0 and (distance >= increase_max or abs(distance-increase_max)<=GLITCH_ALLOWANCE):
                    if state == 1:
                        if float(group[o][1])!=rear_value:
                            min_rear_value = float(group[o][1])
                    increase_count += 1
                    increase_max = distance
                    state = 2
                    if distance == previous_value:
                        repeat += 1
                    else : 
                        repeat = 0
                previous_value = float(group[o][1])
                
            front_value_ratio = front_value/(front_value+rear_value)
            rear_value_ratio = rear_value/(front_value+rear_value)
            decrease_count_ratio = decrease_count/(decrease_count+increase_count)
            increase_count_ratio = increase_count/(decrease_count+increase_count)
            min_front_ratio = min_front_value/(min_front_value+min_rear_value)
            min_rear_ratio = min_rear_value/(min_front_value+min_rear_value)
            
            enter = 185*rear_value_ratio + 15*decrease_count_ratio + 7*min_front_ratio
            exitt = 185*front_value_ratio + 15*increase_count_ratio + 7*min_rear_ratio

            """
            enter = 0
            exitt = 0
            if front_value < rear_value:
                enter += 1
            elif rear_value < front_value:
                exitt += 1
            if decrease_count > increase_count:
                enter += 1
            elif increase_count > decrease_count:
                exitt += 1
            if min_front_value > min_rear_value:
                enter += 1
            elif min_front_value < min_rear_value:
                exitt += 1
            """  
            if enter > exitt:
                result = group[0][0],'Enter'
            elif enter < exitt:
                result = group[0][0],'Exit'
            else:
                result = group[0][0],'IDK'
            if previous_result != result:
                f.write(str(result))
                f.write("\n")
                previous_result = result
    f.close()