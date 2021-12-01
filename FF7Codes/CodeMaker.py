# This is a python program that apparently generates winning codes according to reddit

from string import ascii_uppercase

codeStart = "0072"
codeMid = "22:"
numRan = range(0,9)
for i in numRan:
    for j in numRan:
        for k in ascii_uppercase:
            for l in ascii_uppercase:
                for m in numRan:
                    for n in numRan:
                        print(codeStart+str(i)+str(j)+k+l+" "+codeMid+str(m)+str(n))
