import math
sumT = 0
n = 5
check = 0

#max loops is n**2/2 (rounded if odd) -1

def sumLoop(limit,count):
    sumHold = []
    sumD = 0

    def recur(limit,count):        
        if count <=0:
            #print(":"+str(limit))
            sumHold.append(limit)
        else:
            for i in range(1,limit):
                #print("-"+str(sumT))
                recur(i,count-1)

    recur(limit,count)

    for i in sumHold:
        sumD += i

    return sumD

print(math.floor(n**2/2)-1)

#0
sumT += 1
print(sumT)

#1
sumT += n**2
print(sumT)

if ((n**2)/2)%1==0:
    check = 1

#2 
for i in range(1,math.floor(n**2/2)-check):
    sumT += sumLoop(n**2,i)
    print(sumT)

#double
sumT = sumT*2
print(sumT)

if check == 1:
    sumT += sumLoop(n**2, math.floor(n**2/2)-check)
    print(sumT)
