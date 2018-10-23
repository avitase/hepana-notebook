from math import sqrt

def armenteros(p1, p2):
    mother = [a+b for a, b in zip(p1, p2)]

    prod = lambda v1, v2: sum([a*b for a, b in zip(v1, v2)])
    mag_mother = sqrt(prod(mother, mother))
    ql = lambda p: prod(mother, p) / mag_mother

    ql1 = ql(p1)
    ql2 = ql(p2)

    alpha = (ql1 - ql2) / (ql1 + ql2)
    qt = sqrt(prod(p1, p1) - ql1*ql1)
    
    return (alpha, qt)
