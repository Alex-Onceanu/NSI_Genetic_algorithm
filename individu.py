import pygame
from random import randint

from pygame import math 
from ModuleUtile import Clamp, Equilibrer_pourcentages
from resolution import RESOLUTION_X, RESOLUTION_Y
from neurone import Neurone
class Individu:
    def __init__(self, __neurone_horizontal:Neurone, __neurone_vertical:Neurone, __couleur:tuple) -> None:
        self.vitesse_max = 2
        self.couleur = __couleur

        self.neurone_horizontal = __neurone_horizontal
        self.neurone_vertical = __neurone_vertical

        self.rect = pygame.Rect(200,384,18,18)
        self.vitesse:list = [0,0]
        self.compteur_decision = 1

        self.mort = False

    def Mise_A_Jour(self, pos_zone_victoire_x:int, pos_zone_victoire_y:int, touche_victoire:bool) -> None:
        self.__Decision(pos_zone_victoire_x, pos_zone_victoire_y, touche_victoire)

        
        self.rect.left += self.vitesse[0]
        self.rect.top += self.vitesse[1]
        #self.__clampBorder()

    def Afficher(self, fenetre) -> None:
        pygame.draw.rect(fenetre, self.couleur, self.rect, width= 0)
#________________________________privé________________________________________________

    def map_val (self, val, max_val) :
        return 2 * val / max_val - 1

    def __Decision(self, pos_zone_victoire_x:int, pos_zone_victoire_y:int, touche_victoire:bool) -> tuple:
        
        donnees:list = [self.rect.centerx, 
                        self.rect.centery, 
                        self.vitesse[0] / self.vitesse_max,
                        self.vitesse[1] / self.vitesse_max,
                        pos_zone_victoire_x,
                        pos_zone_victoire_y,
                        int(touche_victoire)]
        

        activation = self.neurone_horizontal.Activation(donnees)
        self.vitesse[0] += activation
        self.vitesse[0] = Clamp(self.vitesse[0], -self.vitesse_max, self.vitesse_max)

        activation = self.neurone_vertical.Activation(donnees)
        self.vitesse[1] += activation
        self.vitesse[1] = Clamp(self.vitesse[1], -self.vitesse_max, self.vitesse_max)



    def __clampBorder2(self) -> None:
        if self.rect.right < 0 or self.rect.left > RESOLUTION_X() or self.rect.bottom < 0 or self.rect.top > RESOLUTION_Y():
            self.mort = True

    def __clampBorder2(self) -> None:
        if self.rect.left <= 0 or self.rect.right >= RESOLUTION_X() or self.rect.top <= 0 or self.rect.bottom >= RESOLUTION_Y():
            self.rect.left -= self.vitesse[0]
            self.rect.top -= self.vitesse[1]

    
    
    def Cloner(self):
        return Individu(self.neurone_horizontal.Cloner(), self.neurone_vertical.Cloner(), self.couleur)