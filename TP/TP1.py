import math


def div_euclide():
    a=2026
    b=7
    q= a//b
    r=a%b
    print(q, r)
    print(b*q+r)

def trouve_chiffre():
    u = 123456789%10
    print(u)
    r = (123456789-u)/10
    print(r)

def un_dixieme():
    nb = 0
    for i in range(1000):
        nb += 0.1
    print(100-nb)

def presque_egaux(a, b):
    print(math.isclose(a, b))

def table_mult(x):
    for i in range(11):
        print(f"{x} * {i} = {x * i}")

def calcul_nul():
    res = 0
    for i in range(101):
        res += i
    return res

def nombre_de_chiffre(n):
    res = 1
    while(n > 9):
        unit = n%10
        n -= unit
        n = n/10
        res += 1
    return res

def heron(a, tolerance=1e-12):
    assert  a>=0, "Pas de nombre negatifs, tié fou"
    if a == 0:
        return 0.0
    x = float(a)
    tours = 0
    while True:
        suivant = 0.5 * (x + a / x)
        tours = tours + 1
        if abs(suivant - x) <= tolerance * abs(suivant):
            return suivant
        x = suivant