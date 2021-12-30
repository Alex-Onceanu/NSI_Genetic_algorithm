from math import sqrt

#Ce module contient des fonctions polyvalentes utilisées un peu partout

def Collision(a,b) -> bool:
    #Est-ce que deux rects se croisent
    return a.left < b.right and a.right > b.left and a.bottom > b.top and a.top < b.bottom

def Distance_rects(a,b) -> int:
    #Distance geometrique entre les centres de deux rects
    return sqrt((b.centerx - a.centerx)**2 + (b.centery - a.centery)**2)

def Clamp(v, v_min, v_max):
    #Fait en sorte qu'une valeur v soit comprise entre v_min et v_max, en la "bloquant" entre les bornes
    if v < v_min:
        return v_min
    if v > v_max:
        return v_max
    return v 