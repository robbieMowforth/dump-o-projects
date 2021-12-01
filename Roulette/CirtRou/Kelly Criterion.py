import random

moneyBase = int(input("Enter Amount: "))
#Runs = int(input("How Many Runs: "))

fails1 = 0
fails2 = 0
fails3 = 0
fails4 = 0
fails5 = 0

#( ((2*(18/37))-(19/37))/2 )
avgBetsHold = 0
avgStreakHold = 0
avgDownHold = 0


for k in range (100):
    
    for i in range(1):
        money = moneyBase
        streak = 0
        down = 0
        for j in range(0,100000):
            
            betMain = round(money*((i+2)/100),1)
            betZero = round(betMain/19,1)
            betDouble = round((betMain/19)*18,1)
            money = ( money - betMain )
            if 1/37 < random.random() < 19/37:
                money = money + betDouble*2
            elif random.random() < 1/37:
                money = money + betZero*36
            if money > moneyBase:
                streak+=1
            else:
                down+=1
            #print("Current :"+str(money)+" Bet Amount Zero: "+str(betZero)+" Bet Amount Double: "+str(betDouble)+" Bets Made: "+str(j)+" Streak: "+str(streak))
            try:
                if 4.9/betMain==0.0245:
                    break
            except Exception as e:
                break
        if money > moneyBase:            
            avgBetsHold+=j
            avgBets = avgBetsHold/(k+1)

            avgStreakHold+=streak
            avgStreak = avgStreakHold/(k+1)

            avgDownHold+=down
            avgDown = avgDownHold/(k+1)
            #print("We got :",str(money),"Last bet: ",str(bet),"Chance: ",str((i+2)/100)+" Bets Made: "+str(j)+" Avg Bets Made: "+str(avgBets))
        
        else:
            k-=1
            print("Fail on Chance:",str((i+2)/100))
            if (i+2) == 1:
                fails1+=1
            elif (i+2) == 2:
                fails2+=1
            elif (i+1) == 3:
                fails3+=1
            elif (i+1) == 4:
                fails4+=1
            elif (i+1) == 5:
                fails5+=1
print(" Avg Bets Made: "+str(avgBets)+" Avg Streak On: "+str(avgStreak))
print("1% Fails: "+str(fails1)+", 2% Fails: "+str(fails2)+", 3% Fails: "+str(fails3)+", 4% Fails: "+str(fails4)+", 5% Fails: "+str(fails5))
