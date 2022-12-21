import pandas as pd
df=pd.read_csv("5-1.csv", sep=",")
a=df.iloc[:,1]
a=list(a)
print(a)
num_inout=[]
num_decrease=0
num_increase=0
break_count=0
num_sign=0
#numin=0
#numout=0
alen=len(a)
print(alen)



for i in range(alen-1):
    if i<10:
        continue

    if a[i]-a[i+1]>=2:
        num_decrease+=1
        break_count=0
    if a[i]-a[i+1]<=-2:
        num_increase+=1
        break_count=0
    

    if abs(a[i]-a[i+1])<2:
        break_count+=1
    #print(num_decrease,num_increase,break_count)

    if break_count>3:
        if num_decrease>num_increase:
            num_sign=num_sign+1
            num_decrease=0
            num_increase=0
            break_count=0
            
        elif num_decrease<num_increase:
            num_sign=num_sign-1
            num_decrease=0
            num_increase=0
            break_count=0
        else:
            num_decrease=0
            num_increase=0
            break_count=0


    num_inout.append(num_sign)

print(num_inout)