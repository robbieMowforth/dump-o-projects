import csv

while(True):
    mode=""
    try:
        mode=int(input("1: single number ratio check, 2: up to x number ratio check, "
                        "3: quit program: "))
    except ValueError:
        print("Inputted wrong, try again\n")

    
    if(mode==1):
        number=0
        try:
            number=int(input("input the number you wish to check: "))
            count=0
            for i in range(number):
                if(number%(i+1)==0):
                    count+=1
        
            print("\nYour Number:",number,"    Factor Count:",count,
                  "\nThe ratio of Factor Count to Your Number is: "+
                  str(count/number)+"\nFraction form of ratio: "+str(count)+"/"+str(number)+"\n")
        except ValueError:
            print("Inputted wrong, try again\n")
            
    if(mode==2):
        number=-1
        try:
            number=int(input("input the number you wish the program to go up to: "))
            check=int(input("1: output done in txt file, 2: output done in csv: "))
            if(check==1):
                open("Factor ratio count up to "+str(number)+".txt","w").close()
                outputFile=open("Factor ratio count up to "+str(number)+".txt","w+")
                outputFile.write("Number                        |"
                                 "DivisorCount                   |"
                                 "Ratio Decimal                  |"
                                 "Ratio Fraction                                                                   |\n")

            csvRow=[["Number","Divisor Count"]]
        
            for i in range(number+1):
                print(i)
                count=0
                for j in range(i):
                    if(i%(j+1)==0):
                        count+=1
                if(i!=0 and check==1):
                    fraction=str(count)+"/"+str(i)
                    outputFile.write("% 30d| % 30d| % 30.10f| % 80s|\n" %(i,count,(count/i),fraction))
                elif(i!=0 and check==2):
                    csvRow.append([i,count])

        
            if(check==1):
                print("\ntxt file created\n")
                outputFile.close()
            elif(check==2):
                with open("Factor ratio count up to "+str(number)+".csv","w", newline="") as file:
                    writer=csv.writer(file)
                    writer.writerows(csvRow)
                print("\ncsv file created\n")
            else:
                print("Inputted wrong, try again\n")
                
        except ValueError:
            print("Inputted wrong, try again\n")

    if(mode==3):
        break

                                 
                
        
            
        
            

    
