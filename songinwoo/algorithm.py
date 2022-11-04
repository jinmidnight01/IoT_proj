a=[370,370,370,370,370,370,370,370,370,370,350,330,305,310,250,225,230,180,150,220,280,350,370,370,370,370,370,370,370,370,370,250,220,180,150,170,190,210,230,250,270,290,310,350,370,370,370,370]
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
    if a[i]-a[i+1]>10:
        num_decrease+=1
    if a[i]-a[i+1]<-10:
        num_increase+=1
    

    if abs(a[i]-a[i+1])<2:
        break_count+=1
    print(num_decrease,num_increase,break_count)

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

