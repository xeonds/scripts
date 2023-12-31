from sympy import *
import sys

def f_h(pk1,pk2,conc):
    #variable defination
    h=symbols('h')

    #calculate value
    k1=[10**(-x) for x in pk1]
    k2=[10**(-x) for x in pk2]

    #???
    d11 = (h ** 3) / (h ** 3 + h ** 2 * k1[0] + h * k1[0] * k1[1] + k1[0] * k1[1] * k1[2])
    d21 = (h ** 3) / (h ** 3 + h ** 2 * k2[0] + h * k2[0] * k2[1] + k2[0] * k2[1] * k2[2])

    #solve equation
    return solve(10**(-14)/h+conc[0]* (h ** 2 * k1[0]) / (h ** 3 + h ** 2 * k1[0] + h * k1[0] * k1[1] + k1[0] * k1[1] * k1[2])+2*conc[0]* (h * k1[0] * k1[1]) / (h ** 3 + h ** 2 * k1[0] + h * k1[0] * k1[1] + k1[0] * k1[1] * k1[2])+3*conc[0]* (k1[0] * k1[1] * k1[2]) / (h ** 3 + h ** 2 * k1[0] + h * k1[0] * k1[1] + k1[0] * k1[1] * k1[2])+conc[1]* (h ** 2 * k2[0]) / (h ** 3 + h ** 2 * k2[0] + h * k2[0] * k2[1] + k2[0] * k2[1] * k2[2])+2*conc[1]* (h * k2[0] * k2[1]) / (h ** 3 + h ** 2 * k2[0] + h * k2[0] * k2[1] + k2[0] * k2[1] * k2[2])+3*conc[1]* (k2[0] * k2[1] * k2[2]) / (h ** 3 + h ** 2 * k2[0] + h * k2[0] * k2[1] + k2[0] * k2[1] * k2[2])-h, h)

if __name__ == '__main__':
    if '--info' == sys.argv[1]:
        print('''PH calculate
                ---
                pk11 pk12 pk13;
                pk21 pk22 pk23;
                c1 c2
                ''')
    else:
        data=[int(i) for i in sys.argv[1:9]]
        print(f_h(data[0:3],data[3:6],data[6:8]))