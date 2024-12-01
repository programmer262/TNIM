from math import *
from math import sqrt
def est_premier(n):

    if n % 2 == 0:
        return False
    for i in range(3, int(sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def rotations(n):
    str_n = str(n)
    rot = []
    for i in range(len(str_n)):
        rotated = str_n[i:] + str_n[:i]
        rot.append(int(rotated))
    return rot

def est_premier_circulaire(n):
    if not est_premier(n):
        return False
    
    for rotation in rotations(n):
        if not est_premier(rotation):
            return False
    
    return True