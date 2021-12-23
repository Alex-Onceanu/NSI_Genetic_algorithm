from math import sqrt
from random import randint

def Equilibrer_pourcentages(a,b,c,d,e) -> tuple:
    #Renvoie des pourcentages équilibrés de sorte a ce que leur somme soit de 100%
    #C'est un produit en croix.
    ref = a + b + c + d + e
    if ref == 0: return (20,20,20,20,20)
    return (int(a * 100/ref), int(b * 100/ref), int(c * 100/ref), int(d * 100/ref), int(e*100/ref))

def Collision(a,b) -> bool:
    return a.left < b.right and a.right > b.left and a.bottom > b.top and a.top < b.bottom

def Distance_rects(a,b) -> int:
    #Distance geometrique entre les centres de deux rects
    if Collision(a,b): return 0
    return sqrt((b.center[0] - a.center[0])**2 + (b.center[1] - a.center[1])**2)
