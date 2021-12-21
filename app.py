import pygame
import pygame.time
from monde import Monde


class App:
    def __init__(self, res_x:int, res_y:int) -> None:
        self.RES_X = res_x
        self.RES_Y = res_y
        self.FPS = 60
        self.doit_continuer = True

        pygame.init()
        self.fenetre = pygame.display.set_mode((self.RES_X,self.RES_Y))
        self.chrono = pygame.time.Clock()

        self.monde = Monde()

    def boucle(self) -> None:
        while self.doit_continuer:
            self.monde.Gerer_Evenements(self.Demande_Evenements())
            self.monde.Mise_A_Jour()
            self.monde.Afficher(self.fenetre)

            pygame.display.flip()
            self.chrono.tick(self.FPS)

        pygame.quit()

    def Demande_Evenements(self) -> tuple:
        rep:tuple = (pygame.key.get_pressed(), pygame.event.get())

        for event in rep[1]:
            if event.type == pygame.QUIT :
                self.doit_continuer = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.doit_continuer = False
                break
        return rep
