#What this program is doing is listing all the possible unqiue fractions
#untill infinity (well, attempting too)
Logger=open("Counter.txt","r")
bottom=Logger.read()
bottom=int(bottom)
Logger.close()
TheFile=open("Rational_Infinity_Store.txt","a")
Running=True
for k in range(0,1000):
    for i in range(1,bottom):
        check=True
        if i==1:
            store=str(i)+"/"+str(bottom)+", "
            TheFile.write(str(store))
        for j in range(1,bottom):
            if i%j==bottom%j and j!=1 and i%j<1 and bottom%j<1:
                check=False
        if i%i!=bottom%i and check==True:
                store=str(i)+"/"+str(bottom)+", "
                TheFile.write(store)
    TheFile.write("\n")
    bottom=bottom+1
TheFile.close()

Logger=open("Counter.txt","w")
Logger.write(str(bottom))
Logger.close()
print(bottom)

