#from future import print_function
import math
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)
import sys
sys.stdout = utf8stdout

def sq_equation(a:float,b:float,c:float):
    d=b*b-4*a*c

    if d>0:
        sd = math.sqrt(d)
        x1 = (b-sd)/(2*a)
        x2 = (b+sd)/(2*a)
        return ("two",(x1,x2))
    elif d==0:
        x = b/(2*a)
        return ("one",x)
    else:
        return ("no","Нет рациональных корней")

# Основная программа
a = 100
b = 20
c = -40

#FIXME: Add som informative message
print ("Welcome to experimental branch")

rc,value = sq_equation(a,b,c)
if rc=="one":
    x = value
    print(x)
elif rc=="two":
    x1,x2=value
    print(x1,x2)
else:
    print(value)



