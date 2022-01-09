import pygame
import pygame.time
from monde import Monde
from resolution import RESOLUTION

class App:
    #Classe principale, qui va gérer l'instanciation de la classe Monde 
    def __init__(self) -> None:
        #On va faire 60 frames à chaque seconde (60 FPS), donc la boucle principale est répétée 60 fois à chaque seconde
        self.FPS = 60
        self.doit_continuer = True

        #Initialisation de pygame et de la fenêtre, etc
        pygame.init()
        self.fenetre = pygame.display.set_mode(RESOLUTION())
        self.chrono = pygame.time.Clock()

        self.monde = Monde()

    def boucle(self) -> None:
        #Boucle principale du programme
        while self.doit_continuer:
            #On fait 60 * 10 soit 600 boucles (donc 10 secondes) à chaque génération, avant d'en générer une nouvelle 
            for _ in range(self.FPS * 15):
                if not self.doit_continuer: break

                #Les 3 fonctions les plus importantes de ce programme : elles sont appelées successivement à chaque frame
                # 1) On gère les appuis de touches de clavier (évenements) à partir de la liste d'évenements donnée par pygame
                # 2) On actualise le monde et chaque individu, tous les calculs et décisions sont faites là
                # 3) On affiche tous les éléments graphiques (individus, rects, textes..)

                self.monde.Gerer_Evenements(self.Demande_Evenements())
                self.monde.Mise_A_Jour()
                self.monde.Afficher(self.fenetre)

                #pygame.display.flip() doit être appelée à chaque frame pour actualiser la fenêtre
                pygame.display.flip()
                #On limite le nombre d'itérations par seconde à 60 grâce à pygame
                self.chrono.tick(self.FPS)
            else:
                #C'est une boucle for-else, ce else se déclenche uniquement si aucun "break" n'a été déclenché
                #Après 10 secondes, on crée une nouvelle génération et on recommence à boucler avec les 3 fonctions principales
                self.monde.Nouvelle_Generation()

        #On arrive ici uniquement si l'utilisateur souhaite quitter le programme, donc on ferme pygame et tout
        pygame.quit()

    def Demande_Evenements(self) -> list:
        #Cette fonction vérifie si l'utilisateur veut fermer la fenêtre, et obtient la liste d'évenements qui sera transmise à la suite du programme
        
        #rep est une liste d'évenements, à chaque frame pygame va y mettre toutes les interactions avec l'utilisateur
        #Exemple : appui de la touche W, minimisation de la fenêtre, déplacement de la souris, etc...
        rep:list = pygame.event.get()

        #On peut itérer à travers cette liste et vérifier s'il y a l'évenement qu'on recherche
        for evenement in rep:
            #Si l'utilisateur clique sur la croix de la fenêtre l'évenement pygame.QUIT est ajouté à la liste; s'il est dans rep on quitte le jeu
            if evenement.type == pygame.QUIT :
                self.doit_continuer = False
                break
            #Si l'utilisateur appuie sur la touche ECHAP, quitter le jeu
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_ESCAPE:
                self.doit_continuer = False
                break

        #On retransmet cette liste d'évenements au monde qui pourra itérer aussi
        return rep
