import matplotlib.pyplot as plt
import csv
  
x = []
y = []
  
with open(r'C:\Users\vkstk\OneDrive\바탕 화면\IoT_proj\result.csv','r') as csvfile:
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
  
fig, ax = plt.subplots()
ax.plot(x, y, linewidth = 0.72, label = "Visualize")
plt.xlabel('time')
plt.ylabel('distance')
plt.title('visualization')
ax.legend()
plt.show()
plt.savefig('Name.png')