from sympy import *
import argparse

def solve():
    #variable defination
    h=symbols('h')

    #get variables from input
    pk1 = [int(x) for x in input('Input pk11-pk13(use space to seperate):').split(' ')]
    pk2 = [int(x) for x in input('Input pk21-pk23(use space to seperate):').split(' ')]
    conc = [int(x) for x in input('Input concentration1-2(use space to separate):').split(' ')]

    #calculate value
    k1=[10**(-x) for x in pk1]
    k2=[10**(-x) for x in pk2]

    #???
    d11 = (h ** 3) / (h ** 3 + h ** 2 * k1[0] + h * k1[0] * k1[1] + k1[0] * k1[1] * k1[2])
    d21 = (h ** 3) / (h ** 3 + h ** 2 * k2[0] + h * k2[0] * k2[1] + k2[0] * k2[1] * k2[2])

    #solve equation
    print(solve(10**(-14)/h+conc[0]* (h ** 2 * k1[0]) / (h ** 3 + h ** 2 * k1[0] + h * k1[0] * k1[1] + k1[0] * k1[1] * k1[2])+2*conc[0]* (h * k1[0] * k1[1]) / (h ** 3 + h ** 2 * k1[0] + h * k1[0] * k1[1] + k1[0] * k1[1] * k1[2])+3*conc[0]* (k1[0] * k1[1] * k1[2]) / (h ** 3 + h ** 2 * k1[0] + h * k1[0] * k1[1] + k1[0] * k1[1] * k1[2])+conc[1]* (h ** 2 * k2[0]) / (h ** 3 + h ** 2 * k2[0] + h * k2[0] * k2[1] + k2[0] * k2[1] * k2[2])+2*conc[1]* (h * k2[0] * k2[1]) / (h ** 3 + h ** 2 * k2[0] + h * k2[0] * k2[1] + k2[0] * k2[1] * k2[2])+3*conc[1]* (k2[0] * k2[1] * k2[2]) / (h ** 3 + h ** 2 * k2[0] + h * k2[0] * k2[1] + k2[0] * k2[1] * k2[2])-h, h))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--info', action='store_true', help="查看帮助信息")
    args = parser.parse_args()
    if args.info:
        print('''PH calculate
                ---
                pk11 pk12 pk13;
                pk21 pk22 pk23;
                c1 c2
                ''')