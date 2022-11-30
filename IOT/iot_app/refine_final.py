import csv
import matplotlib.pyplot as plt

fname = r"C:\Users\vkstk\OneDrive\바탕 화면\IoT_proj\IOT\distance.csv"
file = open(fname,'r')
line = csv.reader(file)

MIN_FREQ = 10
STRUCTURE_SIZE = 3 # memory size to store the data
GLITCH_ALLOWANCE = 5 # standard of rate-of-change to determine the data validity
TIME_ALLOWANCE = 0.2
STANDARD_CHANGE_ALLOWANCE = 50
RATIO = 2/3
MIN_CHANGE_ALLOWANCE = 200
REPEAT_ALLOWANCE = 3

def getTimeValue(time) :
    (h,m,s) = time.split(":")
    return int(h)*3600 + int(m)*60 + float(s)

class Mentos :
    # . . .
    # data structue to 
    # 1. abstract requisite data
    # 2. convert requisite data into intuitive form
    # . . .
    # receive data from the sensor directly
    # 1. memory efficient // only STRUCTURE SIZE memory required
    # 2. time efficient // O(1) to receive each essential data
    # . . .
    mentos = [] # storage for the time-distance data
    pre_abstracted_data = []
    abstracted_data = []
    trimmed_data = []
    analyzed_data = []
    
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
            
    def abstract(self):
        # . . .
        # abstract the essential data from the csv file which are sets of 
        # 1. current front fixed-data sample
        # 2. current essential data
        # 3. current rear fixed-data sample
        # . . .
        repeat_count = 0 # to determine whether it's fixed or minimum/maximum
        state = 0 # to remember the previous gradient of the graph
        prev_distance = 0
        
        for time_distance in line :
            # store the data in the structure
            self.enqueue(time_distance)
            
            current_distance = float(self.mentos[-1][1]) 
            # if the gradient is DECREASING
            if (prev_distance - current_distance) >= GLITCH_ALLOWANCE : 
                # and the gradient had been INCREASING
                if state == 2 :
                    # this is a new group after the completed group
                    # so append the completed group to the abstracted_data
                    self.abstracted_data.append(self.pre_abstracted_data)
                    # and empty the temporary list for the new group
                    self.pre_abstracted_data = []
                
                # mark the state as DECREASING
                state = 1
                # if the mentos is NOT full, it means the previous data was appended
                if len(self.mentos) != STRUCTURE_SIZE :
                    # so just append the current data
                    self.pre_abstracted_data.append(self.mentos.pop())
                else : 
                    # if the mentos IS full, it means this is the first essential data
                    # so append the data including
                    # 1. current front fixed-data sample
                    self.pre_abstracted_data.append(self.mentos.pop(-2))
                    # 2. current essential data
                    self.pre_abstracted_data.append(self.mentos.pop())
                
                # the value has changed so reset the count
                repeat_count = 0
            
            # if the gradient is INCREASING
            elif (prev_distance - current_distance) <= -GLITCH_ALLOWANCE:
                # if the graph's been decreasing or increasing, this is a valid value
                if state == 1 or state == 2:
                    # mark the state as INCREASING
                    state = 2
                    # and append the current essential data
                    self.pre_abstracted_data.append(self.mentos.pop())
                # the value has changed so reset the count
                repeat_count = 0
            
            # if the gradient is SIMILIAR   
            else :
                # and the graph has been increasing
                if state == 2 :
                    # and the value repeated enough time to be fixed value
                    if repeat_count >= MIN_FREQ :
                        for i in range(10):
                            self.pre_abstracted_data.pop(-1)
                        # append the group to the abstracted_data
                        self.abstracted_data.append(self.pre_abstracted_data)
                        # and empty the group for the next data
                        self.pre_abstracted_data = []
                        # then reset the count and the state
                        state = 0
                        repeat_count = 0
                        
                    # but can't determine if the value is fixed or just repeated
                    else : 
                        # append the data and count that data just in case
                        repeat_count += 1
                        self.pre_abstracted_data.append(self.mentos.pop())
                        
                # and the graph has been decreasing
                elif state == 1 : 
                    # and the value repeated enough time to be fixed value
                    if repeat_count >= MIN_FREQ :
                        # reset the list, state and the count
                        self.pre_abstracted_data = []
                        state = 0
                        repeat_count = 0
                    # but can't determine if the value is fixed or just repeated
                    else :
                        # append the data and count that data just in case
                        repeat_count += 1
                        self.pre_abstracted_data.append(self.mentos.pop())
            
            #update the previous_distance         
            prev_distance = current_distance
            
        #if the set is not empty after the iteration is over
        if len(self.pre_abstracted_data)!=0:
            for i in range(repeat_count):
                self.pre_abstracted_data.pop()
            self.abstracted_data.append(self.pre_abstracted_data)
    
    def merge(self):
        # . . .
        # merge incomplete groups into the complete one
        # . . .
        i = 0
        
        iteration = len(self.abstracted_data)
        flag = [False for k in range(len(self.abstracted_data))]
        while i < iteration:
            group = self.abstracted_data[i]
            min_data = min([float(j) for i,j in group])
            front_fixed_data = float(group[0][1])
            rear_fixed_data = float(group[-1][1])
            
            # if the graph seems like it didn't reach its edge nor started from the minimum
            if abs(front_fixed_data - rear_fixed_data) > STANDARD_CHANGE_ALLOWANCE :
                current_start_time = getTimeValue(group[0][0][-15:])
                current_end_time = getTimeValue(group[-1][0][-15:])
                front_time_gap = 1000
                rear_time_gap = 1000
                
                if i!=0 :
                    previous_group = self.abstracted_data[i-1]
                    previous_end_time = getTimeValue(previous_group[-1][0][-15:])
                    front_time_gap = abs(previous_end_time - current_start_time)
                    
                if i!=len(self.abstracted_data)-1 :
                    next_group = self.abstracted_data[i+1]
                    next_start_time = getTimeValue(next_group[0][0][-15:])
                    rear_time_gap = abs(next_start_time - current_end_time)
   
                # if the data is closer to the previous data
                if front_time_gap < rear_time_gap and flag[i-1]==False:
                    self.abstracted_data[i-1] += self.abstracted_data.pop(i)
                    flag[i-1] = True
                    i -= 1
                    iteration -= 1
                
                elif front_time_gap > rear_time_gap and flag[i]==False:
                    self.abstracted_data[i] += self.abstracted_data.pop(i+1)
                    flag[i] = True
                    iteration -= 1 
                    
            # if the group graph has abnormal shape (which resembles a straw)
            elif abs(front_fixed_data - min_data) < GLITCH_ALLOWANCE and flag[i-1]==False and i!=0:
                self.abstracted_data[i-1] += self.abstracted_data.pop(i)
                i -= 1
                iteration -= 1
                
            elif abs(rear_fixed_data - min_data) < GLITCH_ALLOWANCE and flag[i]==False and i!=iteration-1:
                self.abstracted_data[i] += self.abstracted_data.pop(i+1)
                iteration -= 1 
            i += 1
    
    def trim(self):
        self.trimmed_data = self.abstracted_data.copy()
        min_set = []
        i = 0
        
        while i < len(self.trimmed_data):
            group = self.trimmed_data[i]
            distance = []
            min_count = 0
            
            for time,data in group:
                distance.append(float(data))
            min_set.append(min(distance))
            
            # counting the minimum-like value in the group
            for data in distance:
                if abs(data-min(distance)) < GLITCH_ALLOWANCE:
                    min_count += 1
            # if minimum-like value exists more than the given ratio, it's not valid  
            if min_count > len(distance)*RATIO:
                self.trimmed_data.pop(i)
                min_set.pop(i)
                i -= 1
            
            # if this is the second value, check the FIRST value
            if i==1:
                if min_set[0] - min_set[1] > MIN_CHANGE_ALLOWANCE:
                    self.trimmed_data.pop(0)
                    min_set.pop(0)
                    i -= 1
            elif i>1:
                # if this is the last value, check the LAST value too
                if (i==len(self.trimmed_data)-1) and (min_set[-1] - min_set[-2] > MIN_CHANGE_ALLOWANCE):
                    self.trimmed_data.pop(-1)
                    min_set.pop(-1)
                    if min_set[-1] - min_set[-2] > MIN_CHANGE_ALLOWANCE:
                        self.trimmed_data.pop(-1)
                        min_set.pop(-1)
                        
                else : 
                    min_standard = min(min_set[i-2], min_set[i])
                    if min_set[i-1] - min_standard > MIN_CHANGE_ALLOWANCE:
                        self.trimmed_data.pop(i-1)
                        min_set.pop(i-1)
                        i -= 1
            i += 1
            
    def inout(self):
        for group in self.trimmed_data: 
            state = 0
            min_data = min([float(j) for i,j in group])
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
            min_front_value =  0
            min_rear_value = 0
            
            # counting the decreasing/increasing data, determining front/rear min data
            for i in range(len(group)):
                distance = float(group[i][1])
                if repeat >= REPEAT_ALLOWANCE:
                    if state == 0 :
                        front_value = previous_value
                    elif state == 2:
                        rear_value = previous_value
                if distance == min_data:
                    if state == 0:
                        if float(group[i-1][1])!=front_value:
                            min_front_value = float(group[i-1][1])
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
                        if float(group[i][1])!=rear_value:
                            min_rear_value = float(group[i][1])
                    increase_count += 1
                    increase_max = distance
                    state = 2
                    if distance == previous_value:
                        repeat += 1
                    else : 
                        repeat = 0
                previous_value = float(group[i][1])

            front_value_ratio = front_value/(front_value+rear_value)
            rear_value_ratio = rear_value/(front_value+rear_value)
            decrease_count_ratio = decrease_count/(decrease_count+increase_count)
            increase_count_ratio = increase_count/(decrease_count+increase_count)
            min_front_ratio = min_front_value/(min_front_value+min_rear_value)
            min_rear_ratio = min_rear_value/(min_front_value+min_rear_value)
            
            # print(rear_value_ratio,front_value_ratio)
            # print(decrease_count_ratio,increase_count_ratio)
            # print(min_front_ratio,min_rear_ratio)
            
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
            # print(enter,exitt)
            # print()
            if enter > exitt:
                self.analyzed_data.append((group[i][0],'Enter'))
            elif enter < exitt:
                self.analyzed_data.append((group[i][0],'Exit'))
            else:
                self.analyzed_data.append((group[i][0],'IDK'))
                
# data = Mentos()

# # 1. total data graph
# x = []
# y = []

# with open(fname,'r') as csvfile:
#     plots = csv.reader(csvfile, delimiter = ',')
     
#     for row in plots:
#         x.append(row[0])
#         y.append(float(row[1]))

# # plt.bar(x, y, color = 'g', width = 0.72, label = "Visualize")
# # plt.xlabel('time')
# # plt.ylabel('distance')
# # plt.title('visualization')
# # plt.legend()
# # plt.show()

# data.abstract()

# # 2. abstracted data graph
# x = []
# y = []
# n=0

# for group in data.abstracted_data :
#     for date_distance in group:
#         x.append(date_distance[0])
#         y.append(float(date_distance[1]))
#     for i in range(3): # to check the group
#         x.append(str(n))
#         y.append(0)
#         n += 1
        
# # plt.bar(x, y, color = 'g', width = 0.72, label = "distance")
# # plt.xlabel('time')
# # plt.ylabel('distance')
# # plt.title('visualization')
# # plt.legend()
# # plt.show()

# data.merge()

# # 3. merged data graph
# x = []
# y = []

# for group in data.abstracted_data :
#     for date_distance in group:
#         x.append(date_distance[0])
#         y.append(float(date_distance[1]))
        
    
# # plt.bar(x, y, color = 'g', width = 0.72, label = "distance")
# # plt.xlabel('time')
# # plt.ylabel('distance')
# # plt.title('visualization')
# # plt.legend()
# # plt.show()

# data.trim()

# # 4. trimmed data graph
# x = []
# y = []
# n = 0

# for group in data.trimmed_data :
#     for date_distance in group:
#         x.append(date_distance[0])
#         y.append(float(date_distance[1]))
#         # print(date_distance)
#     for i in range(3): # to check the group
#         x.append(str(n))
#         y.append(0)
#         n += 1
#     # print()
    
# # plt.bar(x, y, color = 'g', width = 0.72, label = "distance")
# # plt.xlabel('time')
# # plt.ylabel('distance')
# # plt.title('visualization')
# # plt.legend()
# # plt.show()

# data.inout()

# for i in data.analyzed_data:
#     print(i)

# f = open("IOT/result.csv", 'w')
# for i in data.analyzed_data:
#     f.write(str(i)+'\n')
# f.close()

