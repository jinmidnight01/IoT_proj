#algorithm8
import pandas as pd
df=pd.read_csv("7-5.csv", sep=",")

a=df.iloc[:,1]
a=list(a)

num_inout=[]
num_sign=0
big_gradient1=0
big_gradient2=0
big_gradient3=0
big_gradient4=0
big_gradient5=0
small_gradient1=0
small_gradient2=0
small_gradient3=0
small_gradient4=0
small_gradient5=0
break_count=0
alen=len(a)

for i in range(alen-1):
    if i<10:
        num_inout.append(num_sign)
        continue

    if abs(a[i]-a[i+1])>=2:
        break_count=0
        if big_gradient1<a[i+1]-a[i]:
            big_gradient5=big_gradient4
            big_gradient4=big_gradient3
            big_gradient3=big_gradient2
            big_gradient2=big_gradient1
            big_gradient1=a[i+1]-a[i]
        else:
            if big_gradient2<a[i+1]-a[i]:
                big_gradient5=big_gradient4
                big_gradient4=big_gradient3
                big_gradient3=big_gradient2
                big_gradient2=a[i+1]-a[i]
            elif big_gradient3<a[i+1]-a[i]:
                big_gradient5=big_gradient4
                big_gradient4=big_gradient3
                big_gradient3=a[i+1]-a[i]
            elif big_gradient4<a[i+1]-a[i]:
                big_gradient5=big_gradient4
                big_gradient4=a[i+1]-a[i]
            elif big_gradient5<a[i+1]-a[i]:
                big_gradient5=a[i+1]-a[i]

        if small_gradient1>a[i+1]-a[i]:
            small_gradient5=small_gradient4
            small_gradient4=small_gradient3
            small_gradient3=small_gradient2
            small_gradient2=small_gradient1
            small_gradient1=a[i+1]-a[i]
        else:
            if small_gradient2>a[i+1]-a[i]:
                small_gradient5=small_gradient4
                small_gradient4=small_gradient3
                small_gradient3=small_gradient2
                small_gradient2=a[i+1]-a[i]
            elif small_gradient3>a[i+1]-a[i]:
                small_gradient5=small_gradient4
                small_gradient4=small_gradient3
                small_gradient3=a[i+1]-a[i]
            elif small_gradient4>a[i+1]-a[i]:
                small_gradient5=small_gradient4
                small_gradient4=a[i+1]-a[i]
            elif small_gradient5>a[i+1]-a[i]:
                small_gradient5=a[i+1]-a[i]


    if abs(a[i]-a[i+1])<2:
        break_count+=1

    print(big_gradient1, big_gradient2,big_gradient3,big_gradient4,big_gradient5,
          small_gradient1, small_gradient2,small_gradient3,small_gradient4,small_gradient5 ,num_sign)
    if break_count>7:
        break_count=0
        if small_gradient2==0 or big_gradient2==0:
            small_gradient2=0
            big_gradient2=0
        if small_gradient3==0 or big_gradient3==0:
            small_gradient3=0
            big_gradient3=0
        if small_gradient4==0 or big_gradient4==0:
            small_gradient4=0
            big_gradient4=0
        if small_gradient5==0 or big_gradient5==0:
            small_gradient5=0
            big_gradient5=0

        if abs(big_gradient1+big_gradient2+big_gradient3+0.95*big_gradient4+0.95*big_gradient5)/5>abs(small_gradient1+small_gradient2+small_gradient3+0.95*small_gradient4+0.95*small_gradient5)/5:
            print(abs(big_gradient1+big_gradient2+big_gradient3+0.95*big_gradient4+0.95*big_gradient5)/5,
                  abs(small_gradient1+small_gradient2+small_gradient3+0.95*small_gradient4+0.95*small_gradient5)/5)
            num_sign+=1
            big_gradient1=0
            big_gradient2=0
            big_gradient3=0
            big_gradient4=0
            big_gradient5=0
            small_gradient1=0
            small_gradient2=0
            small_gradient3=0
            small_gradient4=0
            small_gradient5=0
            
            for j in range(1,7):
                num_inout[i-j]=num_sign
        elif abs(big_gradient1+big_gradient2+big_gradient3+0.95*big_gradient4+0.95*big_gradient5)/5<abs(small_gradient1+small_gradient2+small_gradient3+0.95*small_gradient4+0.95*small_gradient5)/5:
            print(abs(big_gradient1+big_gradient2+big_gradient3+0.95*big_gradient4+0.95*big_gradient5)/5,
                  abs(small_gradient1+small_gradient2+small_gradient3+0.95*small_gradient4+0.95*small_gradient5)/5)
            num_sign-=1
            big_gradient1=0
            big_gradient2=0
            big_gradient3=0
            big_gradient4=0
            big_gradient5=0
            small_gradient1=0
            small_gradient2=0
            small_gradient3=0
            small_gradient4=0
            small_gradient5=0
            
            for j in range(1,7):
                num_inout[i-j]=num_sign
        else:
            #print(abs(1.1*big_gradient1+big_gradient2+big_gradient3)/3,abs(1.1*small_gradient1+small_gradient2+small_gradient3)/3)
            big_gradient1=0
            big_gradient2=0
            big_gradient3=0
            big_gradient4=0
            big_gradient5=0
            small_gradient1=0
            small_gradient2=0
            small_gradient3=0
            small_gradient4=0
            small_gradient5=0

    num_inout.append(num_sign)       
print(num_inout) 