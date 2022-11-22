import matplotlib.pyplot as plt
import csv
  
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