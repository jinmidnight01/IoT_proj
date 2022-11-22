import csv
import matplotlib.pyplot as plt

file = open(r'C:\Users\Pearl\Desktop\IoT\Codes\experiment\(3) 교육과학관\1.csv','r')
line = csv.reader(file)

MIN_FREQ = 5
STRUCTURE_SIZE = 3 # memory size to store the data
GLITCH_ALLOWANCE = 5 # standard of rate-of-change to determine the data validity
TIME_ALLOWANCE = 0.2
STANDARD_CHANGE_ALLOWANCE = 60

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
    isValid =  0
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
            if (prev_distance - current_distance) > GLITCH_ALLOWANCE : 
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
            elif (prev_distance - current_distance) < -GLITCH_ALLOWANCE:
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
    
    def merge(self):
        # . . .
        # merge incomplete groups into the complete one
        # . . .
        i = 0
        iteration = len(self.abstracted_data)
        while i < iteration:
            group = self.abstracted_data[i]
            front_fixed_data = float(group[0][1])
            rear_fixed_data = float(group[-1][1])
            
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
                if front_time_gap < rear_time_gap :
                    self.abstracted_data[i-1] += self.abstracted_data.pop(i)
                    i -= 1
                    iteration -= 1
                
                elif front_time_gap > rear_time_gap :
                    self.abstracted_data[i] += self.abstracted_data.pop(i+1)
                    iteration -= 1   
            i += 1
        
    def trim(self):
        # . . .
        # eliminate the glitch and dummy end-data
        # . . . 
        distance_gap = []
        distance = []
        for group in self.abstracted_data : 
            for date_distance in group :
                distance.append(float(date_distance[1]))
            gap = max(distance) - min(distance)
            distance_gap.append(gap)
            distance = []
            
        minimum_gap = max(distance_gap)/3
        for i in range(len(distance_gap)):
            if distance_gap[i] > minimum_gap:
                self.trimmed_data.append(self.abstracted_data[i])
                
        for group in self.trimmed_data : 
            rear_fixed_data = float(group[-1][1])
            while abs(rear_fixed_data - float(group[-1][1])) < GLITCH_ALLOWANCE:
                group.pop(-1)
                
    def inout(self):
        # . . .
        # determine whether the group indicates enter or exit
        # . . .    
        for group in self.trimmed_data : 
            distance = []
            decrease = 0
            increase = 0
            state = 0
            
            for date_distance in group :
                distance.append(float(date_distance[1]))
        
            for dist in distance : 
                if dist == min(distance):
                    state = 1
                elif state == 0:
                    decrease += 1
                elif state == 1:
                    state == 2
                    increase += 1
                elif state == 2:
                    increase += 1
                    
            if increase > decrease : 
                self.analyzed_data.append('Exit')
                
            elif increase < decrease : 
                self.analyzed_data.append('Enter')
                        
data = Mentos()
data.abstract()
data.merge()
data.trim()
data.inout()

####################################visualization####################################
# 1. total data graph
x = []
y = []
  
with open(r'C:\Users\Pearl\Desktop\IoT\Codes\experiment\(3) 교육과학관\1.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
      
    for row in plots:
        x.append(row[0])
        y.append(float(row[1]))

plt.bar(x, y, color = 'g', width = 0.72, label = "Visualize")
plt.xlabel('time')
plt.ylabel('distance')
plt.title('visualization')
plt.legend()
plt.show()

# 2. abstracted data graph
x = []
y = []
for group in data.abstracted_data :
    for date_distance in group:
        print(date_distance)
        x.append(date_distance[0])
        y.append(float(date_distance[1]))
    print()
plt.bar(x, y, color = 'g', width = 0.72, label = "distance")
plt.xlabel('time')
plt.ylabel('distance')
plt.title('visualization')
plt.legend()
plt.show()

# 3. trimmed data graph
x = []
y = []
for group in data.trimmed_data :
    for date_distance in group:
        #print(date_distance)
        x.append(date_distance[0])
        y.append(float(date_distance[1]))
    print()
plt.bar(x, y, color = 'g', width = 0.72, label = "distance")
plt.xlabel('time')
plt.ylabel('distance')
plt.title('visualization')
plt.legend()
plt.show()

# 4. analyzed data 
for i in data.analyzed_data:
    print(i)
