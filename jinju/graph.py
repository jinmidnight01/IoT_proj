import matplotlib.pyplot as plt
import csv
  
x = []
y = []
  
with open(r'C:\Users\Pearl\Desktop\IoT\result.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
    sum = 0
    for row in plots:
        
        if row[1][2:-2]=='Exit' :
            sum -= 1
        elif row[1][2:-2]=='Enter':
            sum += 1
        print(row[1][1:-1])
        x.append(row[0][-16:21])
        y.append(sum)
  
plt.bar(x, y, color = 'g', width = 0.72, label = "Visualize")
plt.xlabel('time')
plt.ylabel('distance')
plt.title('visualization')
plt.legend()
plt.show()