from random import randint

import pygame

from ModuleUtile import File
from individu import Individu


class Monde:
    def __init__(self) -> None:
        self.population = File()
        self.nb_individus = 20
        
        for _ in range(self.nb_individus):
            p = Individu(randint(1,509))
            self.population.Enfiler(p)

    def Gerer_Evenements(self, evenements:tuple) -> None:
        for _ in range(self.nb_individus):
            individu = self.population.Defiler()
            individu.Gerer_Evenements(evenements)
            self.population.Enfiler(individu)

    def Mise_A_Jour(self) -> None:
        for _ in range(self.nb_individus):
            individu = self.population.Defiler()
            individu.Mise_A_Jour()
            self.population.Enfiler(individu)

    def Afficher(self, fenetre) -> None:
        fenetre.fill((255,255,255))
        for _ in range(self.nb_individus):
            individu = self.population.Defiler()
            individu.Afficher(fenetre)
            self.population.Enfiler(individu)