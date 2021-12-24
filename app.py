import pygame
import pygame.time
from monde import Monde
from resolution import RESOLUTION

class App:
    def __init__(self) -> None:
        self.FPS = 60
        self.doit_continuer = True

        pygame.init()
        self.fenetre = pygame.display.set_mode(RESOLUTION())
        self.chrono = pygame.time.Clock()

        self.monde = Monde()

    def boucle(self) -> None:
        while self.doit_continuer:
            for _ in range(self.FPS * 10):
                if not self.doit_continuer: break

                self.monde.Gerer_Evenements(self.Demande_Evenements())
                self.monde.Mise_A_Jour()
                self.monde.Afficher(self.fenetre)

                pygame.display.flip()
                self.chrono.tick(self.FPS)
            else:
                self.monde.Nouvelle_Generation()

        pygame.quit()

    def Demande_Evenements(self) -> tuple:
        rep:tuple = (pygame.key.get_pressed(), pygame.event.get())

        for evenement in rep[1]:
            if evenement.type == pygame.QUIT :
                self.doit_continuer = False
                break
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_ESCAPE:
                self.doit_continuer = False
                break
        return rep
