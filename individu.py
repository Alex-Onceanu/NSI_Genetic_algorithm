import pygame
from random import randint
from ModuleUtile import Polynome

def Couleur_selon_allele(a) -> tuple:
    return (a%255,abs(a-255)%255,abs(a-510)%255)

class Individu:
    def __init__(self, allele:int) -> None:
        self.__allele = allele
        self.rect = pygame.Rect(100,384,20,20)
        self.couleur:tuple = Couleur_selon_allele(self.__allele)
        self.de = allele
        self.de2 = allele+10
        self.cooldown_ref = (int(Polynome(self.__allele))%11)+20
        self.cooldown = 1

    def Gerer_Evenements(self, evenements:tuple) -> None:
        pass

    def Mise_A_Jour(self) -> None:
        self.cooldown -= 1
        if self.cooldown == 0:
            self.de = (Polynome(self.de)%5) - 2
            self.de2 = (Polynome(self.de2)%5) - 2
            self.cooldown = self.cooldown_ref

        self.rect.left += self.de
        self.rect.top += self.de2
        self.clampBorder()

    def Afficher(self, fenetre) -> None:
        pygame.draw.rect(fenetre, self.couleur, self.rect, width = 0)
        
    def clampBorder(self):
        if self.rect.left < 0:
            self.rect.left += 3
        if self.rect.right > 1366:
            self.rect.left -= 3
        if self.rect.top < 0:
            self.rect.top += 3
        if self.rect.bottom > 768:
            self.rect.top -= 3
