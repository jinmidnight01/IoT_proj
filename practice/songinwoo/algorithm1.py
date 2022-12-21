import pandas as pd
df=pd.read_csv("6-1.csv", sep=",")

a=df.iloc[:,1]
a=list(a)
#print(a)
decreasing=0
increasing=0
stay_increase=0
stay_decrease=0
num_inout=[]
num_decrease=0
num_increase=0
break_count=0
num_sign=0
#numin=0
#numout=0
alen=len(a)
#print(alen)



for i in range(alen-1):
    if i<10:
        num_inout.append(num_sign)
        continue

    if a[i]-a[i+1]>=2:
        num_decrease+=1
        break_count=0
        decreasing=1
        increasing=0
        num_increase=num_increase-stay_increase
        stay_decrease=0
        stay_increase=0

    if a[i]-a[i+1]<=-2:
        num_increase+=1
        break_count=0
        decreasing=0
        increasing=1
        num_decrease=num_decrease-stay_decrease
        stay_decrease=0
        stay_increase=0
        
    
    if a[i]-a[i+1]<2 and decreasing==1:
        num_decrease+=1
        stay_decrease+=1

    if a[i]-a[i+1]>-2 and increasing==1:
        num_increase+=1
        stay_increase+=1
        
    #print(num_decrease, num_increase)
        
    

    if abs(a[i]-a[i+1])<2:
        break_count+=1
    #print(num_decrease,num_increase,break_count)

    if break_count>7:
        
        num_increase=num_increase-stay_increase
        stay_increase=0
        if num_decrease>num_increase:
            
            num_sign=num_sign+1
            num_decrease=0
            num_increase=0
            break_count=0
            decreasing=0
            increasing=0
            for j in range(1,7):
                num_inout[i-j]=num_sign
            
        elif num_decrease<num_increase:
            num_sign=num_sign-1
            num_decrease=0
            num_increase=0
            break_count=0
            decreasing=0
            increasing=0
            for j in range(1,7):
                num_inout[i-j]=num_sign
        else:
            num_decrease=0
            num_increase=0
            break_count=0
            decreasing=0
            increasing=0
            for j in range(1,7):
                num_inout[i-j]=num_sign


    num_inout.append(num_sign)

print(num_inout)