import csv

file = open(r'C:\Users\Pearl\Desktop\IoT\Codes\(1) semina_experiment\1-1.csv','r')
line = csv.reader(file)

STRUCTURE_SIZE = 5
GLITCH_ALLOWANCE = 3
VALID_INDICATOR = 1
MIN_FREQ = 5
MAX_TIME = 2
MIN_SIZE = 8

WEIGHT = 0


def getStandard() :
    # . . .
    # return the value that repeats more than MIN_FREQ = 5 times
    # . . .
    countDown = 0
    standard = float(next(line)[1])
    while countDown < MIN_FREQ :
        temp = float(next(line)[1])
        if abs(temp-standard) < GLITCH_ALLOWANCE :
            countDown += 1
        else : 
            countDown = 0
        standard = temp
    return standard

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
    ifValid = 0
    mentos = []
    abstracted_data = []
    pre_group = []
    grouped_data = []
    intuitive_data = []
        
    def abstract(self): # 1 function
        for time_distance in line :
            # enqueue the lastest data into the structure
            self.mentos.append(time_distance)
            # dequeue the oldest data if the structure is FULL
            if len(self.mentos) > STRUCTURE_SIZE :
                self.mentos.pop(0)
            
            current_distance = float(self.mentos[-1][1])
            if abs(current_distance - STANDARD) > GLITCH_ALLOWANCE : 
                self.ifValid = 1
                if len(self.mentos) != STRUCTURE_SIZE : 
                    self.abstracted_data.append(self.mentos.pop())
                else : 
                    self.abstracted_data.append(self.mentos.pop(-2))
                    self.abstracted_data.append(self.mentos.pop())
                    
            elif self.ifValid == 1 : 
                self.ifValid = 0
                self.abstracted_data.append(self.mentos.pop())
              
    def group(self): #grouping the data originated from the same person
        lastest_time = getTimeValue(self.abstracted_data[0][0][-15:])
        for time_distance in self.abstracted_data : 
            current_time = getTimeValue(time_distance[0][-15:])
            
            if abs(lastest_time - current_time) > VALID_INDICATOR:
                time_spent = abs(getTimeValue(self.pre_group[0][0][-15:]) - getTimeValue(self.pre_group[-1][0][-15:]))
                if time_spent > MAX_TIME :
                    self.pre_group = self.divide(self.pre_group)
                    for group in self.pre_group :
                        self.grouped_data.append(group)
                else :
                    self.grouped_data.append(self.pre_group)
                self.pre_group = []
            self.pre_group.append(time_distance)
            lastest_time = current_time
            

        time_spent = abs(getTimeValue(self.pre_group[0][0][-15:]) - getTimeValue(self.pre_group[-1][0][-15:]))
        if time_spent > MAX_TIME :
            self.pre_group = self.divide(self.pre_group)
            for group in self.pre_group :
                self.grouped_data.append(group)
        else :
            #upload the last group into the grouped_data list
            self.grouped_data.append(self.pre_group)
        self.pre_group = []
        
    def divide(self, multiple): #dividing the single multiple-people group into multiple groups
        smaller_group = []
        divided_group = []
        slopeChange = -1
        prev_distance = 1000

        for time_distance in multiple :
            current_distance = float(time_distance[1])

            if prev_distance >= current_distance :
                if abs(prev_distance - current_distance) > GLITCH_ALLOWANCE and slopeChange == 1:
                    divided_group.append(smaller_group)
                    smaller_group = []
                    smaller_group.append(divided_group[-1][-1]) 
                    slopeChange = -1
                prev_distance = current_distance
                
            else : 
                slopeChange = 1
                prev_distance = current_distance
            smaller_group.append(time_distance) 
        
        divided_group.append(smaller_group)
        
        return divided_group
    
    def merge(self): # merging too-small groups into bigger groups
        for i in range(len(self.grouped_data)) : 
            if len(self.grouped_data[i])<=MIN_SIZE :
                if i!=0 and i!=len(self.grouped_data)-1 : 
                    if abs(float(self.grouped_data[i-1][-1][1])-STANDARD) >= abs(float(self.grouped_data[i+1][0][1])-STANDARD):
                        self.grouped_data[i-1] += self.grouped_data[i]     
                    else : 
                        self.grouped_data[i+1] += self.grouped_data[i]
                elif i==0:
                    self.grouped_data[i+1] += self.grouped_data[i]
                elif i==len(self.grouped_data)-1:
                    self.grouped_data[i-1] += self.grouped_data[i]
                self.grouped_data.pop(i)
            if i==len(self.grouped_data)-1 :
                break
                
    def convert(self): # 2 function
        for group in self.grouped_data:
            min = 1000
            decrease_count = 0
            increase_count = 0
            
            for i in range(len(group)) : 
                distance = float(group[i][1])
                if abs(distance-STANDARD) > GLITCH_ALLOWANCE or i==0 or i==len(group)-1:
                    if min > distance :
                        min = distance
                        decrease_count += 1
                    elif min < distance :
                        increase_count += 1

            ###################### changeable weight on count ######################   
            #increase = float(group[0][1]) - float(group[1][1])*0
            #decrease = float(group[-1][1]) - float(group[-2][1])*0
            
            #increase = float(group[0][1])*0 - float(group[1][1]) 
            #decrease = float(group[-1][1])*0 - float(group[-2][1]) 
            
            #increase = float(group[0][1]) - float(group[1][1])
            #decrease = float(group[-1][1]) - float(group[-2][1])
            
            increase = float(group[0][1]) - float(group[1][1])*0.5
            decrease = float(group[-1][1]) - float(group[-2][1])*0.5

            #########################################################################

            #increase = (float(group[0][1]) - float(group[1][1]))*increase_count
            #decrease = (float(group[-1][1]) - float(group[-2][1]))*decrease_count
            
            if decrease > increase: 
                self.intuitive_data.append('Enter')
            else :
                self.intuitive_data.append('Exit')
                
                
                
STANDARD = getStandard()
data = Mentos()
data.abstract()
data.group()
data.merge()
data.convert()
 
# test code

print(data.intuitive_data)
"""
for i in data.grouped_data : 
    for j in i :
        print(j)
    print()
"""
file.close()

# when we eliminate every standard-like data, we don't have to care about the in-data glitch