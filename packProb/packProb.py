import decimal
import sys

#For the ratio, we want to look at the number of packs opened to percentage finished
#What is the best number of packs to open to get the best dupes/(packs*itemsPerPack)


completeSet=12
packs=28
itemsPerPack=1

#============================================Math Way#
decimal.getcontext().prec = 100

print(sys.getrecursionlimit())
sys.setrecursionlimit(1500)

def fact(n):
  return 1 if (n==0 or n==1) else n*fact(n-1)

def chooseFunc(n,x):
    return (fact(n))/(fact(n-x)*fact(x))

def pieCalc(n,x,t):
    #n=decimal.Decimal(n)
    #x=decimal.Decimal(x)
    #t=decimal.Decimal(t)
    
    sumPIE=(chooseFunc(n,x)**t)
    #print(sumPIE)
    for i in range(n):
        if i+1==n:
            continue
        elif i%2==0:
            sumPIE-=chooseFunc(n,i+1)*(chooseFunc(n-(i+1),x)**t)
            #print(sumPIE/(chooseFunc(n,x)**t))
        else:
            sumPIE+=chooseFunc(n,i+1)*(chooseFunc(n-(i+1),x)**t)
            #print(sumPIE/(chooseFunc(n,x)**t))

    return sumPIE/(chooseFunc(n,x)**t)

print(pieCalc(completeSet,itemsPerPack,packs))        

#============================================RE-crete Method#
import random

def packArrayClean(packArray,completeSet):
    packArray=[]
    for i in range(completeSet):
        packArray.append(1)
    return packArray

def average(lst):
  return sum(lst) / len(lst)

def simMethod(completeSet,packs,itemsPerPack):  
    packArray=[]
    confidence=100000
    averageHold=[]
    ratioHold=[]
    dupesHold=[]
    for i in range(confidence):
        packArray=packArrayClean(packArray,completeSet)
        amountGotten=0
        dupes=0
        for j in range(packs):
            for k in range(itemsPerPack):
                temp=random.choice(packArray)
                if temp==1:
                    amountGotten+=1
                    #print(str(amountGotten)+"test")
                    packArray[amountGotten-1]=0
                else:
                  continue
        #print(str(amountGotten)+"Large")
        #print(packArray)
        #print(averageHold)
        averageHold.append(amountGotten)
        
        ratioHold.append((packs-amountGotten)/packs)
        dupesHold.append(packs-amountGotten)

    compCount=0
    for i in averageHold:
        if i==completeSet:
            compCount+=1
            
    finalCount=compCount/len(averageHold)

    print("Sim Calc Average Completion: "+str(average(averageHold)))
    print("Sim Calc Ratio: "+str(average(ratioHold)))
    print("Sim Calc Ratio: "+str(average(averageHold)/completeSet))
    print("Sim Calc Dupes Gotten: "+str(average(dupesHold)))
    #print(finalCount)

    #============================================Maths#

    #print(sys.getrecursionlimit())
    sys.setrecursionlimit(1500)

    def fact(n):
      return 1 if (n==0 or n==1) else n*fact(n-1)

    def chooseFunc(n,x):
        return (fact(n))/(fact(n-x)*fact(x))

    def pieCalc(n,x,t):
        
        sumPIE=(chooseFunc(n,x)**t)
        #print(sumPIE)
        for i in range(n):
            if i+1==n:
                continue
            elif i%2==0:
                sumPIE-=chooseFunc(n,i+1)*(chooseFunc(n-(i+1),x)**t)
                #print(sumPIE/(chooseFunc(n,x)**t))
            else:
                sumPIE+=chooseFunc(n,i+1)*(chooseFunc(n-(i+1),x)**t)
                #print(sumPIE/(chooseFunc(n,x)**t))

        return sumPIE/(chooseFunc(n,x)**t)

    print("Maths Calc % Complete Set: "+str(pieCalc(completeSet,itemsPerPack,packs))) 


startPack=0
for i in range(30):
  print("\n===TEST with "+str(i+startPack+1)+" packs===")
  simMethod(completeSet,i+startPack+1,itemsPerPack)


















