import pygame
from random import randint 
from ModuleUtile import Equilibrer_pourcentages
from resolution import RESOLUTION_X, RESOLUTION_Y
class Individu:
    def __init__(self, __p_gauche:int, __p_droite:int, __p_haut:int, __p_bas:int, __p_stop:int, __vitesse_max:int, __taux_decision:int, __couleur:tuple) -> None:
        self.p_gauche, self.p_droite, self.p_haut, self.p_bas, self.p_stop = Equilibrer_pourcentages(__p_gauche,__p_droite,__p_haut,__p_bas,__p_stop)
        self.vitesse_max = __vitesse_max
        self.taux_decision = __taux_decision
        self.couleur = __couleur

        self.rect = pygame.Rect(200,384,18,18)
        self.vitesse:list = [0,0]
        self.compteur_decision = 1

        self.mort = False

    def Cloner(self):
        return Individu(self.p_gauche,self.p_droite,self.p_haut,self.p_bas,self.p_stop,self.vitesse_max,self.taux_decision,self.couleur)

    def Vitesse_Pour_Direction(self, direction:int) -> None:
        if direction == 0:
            self.vitesse = [0,0]
            return
        if direction == 1 or direction == 3:
            self.vitesse[int(direction > 2)] = -self.vitesse_max
            return
        self.vitesse[int(direction > 2)] = self.vitesse_max

    def Decision(self) -> None:
        de = randint(0,100)
        probas = [self.p_stop, self.p_gauche, self.p_droite, self.p_haut, self.p_bas]
        decroissant = sorted(probas, reverse=True)
        for i in decroissant:
            if de <= i:
                self.Vitesse_Pour_Direction(probas.index(i))
                return None
            de -= i
        return None

    def Mise_A_Jour(self) -> None:
        self.compteur_decision -= 1
        if self.compteur_decision <= 0:
            self.compteur_decision = self.taux_decision
            self.vitesse = [0,0]
            self.Decision()
            self.Decision()

        self.rect.left += self.vitesse[0]
        self.rect.top += self.vitesse[1]
        self.clampBorder()

    def clampBorder2(self) -> None:
        if self.rect.right < 0 or self.rect.left > RESOLUTION_X() or self.rect.bottom < 0 or self.rect.top > RESOLUTION_Y():
            self.mort = True

    def clampBorder(self) -> None:
        if self.rect.left <= 0 or self.rect.right >= RESOLUTION_X() or self.rect.top <= 0 or self.rect.bottom >= RESOLUTION_Y():
            self.rect.left -= self.vitesse[0]
            self.rect.top -= self.vitesse[1]

    def clampBorder2(self):
        if self.rect.left < 0:
            self.rect.left = RESOLUTION_X() - self.rect.width
        if self.rect.right > RESOLUTION_X():
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = RESOLUTION_Y() - self.rect.height
        if self.rect.bottom > RESOLUTION_Y():
            self.rect.top = 0

    def Afficher(self, fenetre) -> None:
        pygame.draw.rect(fenetre, self.couleur, self.rect, width= 0)
    