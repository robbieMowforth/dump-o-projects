n=0
list_n=[]
while n<360:
    a=1
    temp=360/(n+1)
    while temp%1>0:
        a=a+1
        temp=(360*a)/(n+1)
    temp=int(temp)
    temp=str(temp)
    list_n.append(temp)
    print(temp)
    n=n+1
StringList_n=", ".join(list_n)
print(StringList_n)
    
