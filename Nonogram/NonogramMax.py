#we get rid of the minuses for rach for loop in the early design because
#each for loop lowers the loop count by 1 due to how the range function works

#this was needed when we learn about the issue with dividing the square root of an odd number
import math

#varible for count
sumT = 0
#varible for length size CHANGE TO GET DIFFERENT RESULTS
n = 4
#varible for width size CHANGE TO GET DIFFERENT RESULTS
q = 4
#varible used to count the number of iterations
check = 0
#half the square of n minus ONE is the highest amount of loops you will need

def sumLoop(limit,count):
    sumHold = []
    sumD = 0

    def recurse(limit,count):
        if count<=0:
            #print(":"+str(limit))
            sumHold.append(limit)
        else:
            for i in range(1,limit):
                recurse(i,count-1)

    recurse(limit,count)
    
    for i in sumHold:
        sumD += i
    return sumD

#0
sumT += 1
print(sumT)

#1
sumT += n*q
print(sumT)

if ((n*q)/2)%1==0:
    check = 1

print(str(math.floor((n*q)/2)-1))

for i in range(1,(math.floor((n*q)/2))-check):
    print(i)
    sumT += sumLoop(n*q,i)
    print(sumT)

#reverse
sumT = 2*sumT
print(sumT)

if check == 1:
    sumT += sumLoop(n**2,(math.floor((n*q)/2))-check)
    print(sumT)
