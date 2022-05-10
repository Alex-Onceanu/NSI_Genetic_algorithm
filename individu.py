import pygame

from ModuleUtile import Clamp
from neurone import Neurone
class Individu:
    #Chaque individu est un petit carré coloré à l'écran qui doit savoir prendre une décision et décider d'où aller
    #Le but est qu'une population d'individus "apprenne" à se rendre dans une zone de victoire et y rester
    def __init__(self, __neurone_horizontal:Neurone, __neurone_vertical:Neurone, __couleur:tuple) -> None:
        
        self.vitesse_max = 2
        self.couleur = __couleur

        #Pour pouvoir prendre des décisions, chaque individu a 2 neurones (voir classe Neurone)
        #En fonction des paramètres donnés (Donc la distance par rapport a la zone par exemple) et des coefficients de ses neurones l'individu se deplacera dans une certaine direction
        #Un neurone pour savoir si l'individu doit aller en haut ou en bas, un autre neurone pour gauche-droite
        self.neurone_vertical = __neurone_vertical
        self.neurone_horizontal = __neurone_horizontal
    
        #Un rect est une structure de pygame qui contient simplement une position (x ; y) et une taille (longueur et largeur)
        #C'est ce rect qui sera affiché à la fin de chaque frame, donc la position de l'individu est ici
        self.rect = pygame.Rect(200,384,18,18)
        #Sauvegarde de l'ancienne position de l'individu, sert pour les collisions (voir gestion des collisions)
        #Cette sauvegarde se fait a chaque appel de Mise_A_Jour, et l'individu est renvoyé à sa sauvegarde en cas de collision
        self.position_frame_precedente:tuple = (self.rect.left, self.rect.top)

        #A la fin de chaque Mise_A_Jour, on ajoute à la position de l'individu sa vitesse x et y
        self.vitesse:list = [0,0]

        self.mort = False

    def Mise_A_Jour(self, pos_zone_victoire_x:int, pos_zone_victoire_y:int, cogne) -> None:
        #On sauvegarde l'ancienne position, l'individu y revient s'il se mange un mur
        self.position_frame_precedente = (self.rect.left, self.rect.top)

        #A chaque frame, l'individu prend une décision : en fonction de la distance le séparant de la zone de victoire il va se donner une certaine vitesse x et y
        #cogne est une information supplémentaire qu'il transmet a ses neurones : 1000 si l'individu touche un obstacle, sinon 0
        #(1000 car les autres données sont entre 0 et RESOLUTION_X(), donc si on ajoute juste 1 ça n'aura aucun impact)
        self.__Decision(pos_zone_victoire_x, pos_zone_victoire_y, int(cogne)*1000)

        #On ajoute sa vitesse à sa position, pour obtenir sa nouvelle position
        #La vitesse est comprise entre [-2, -2] (vers haut-gauche) et [2, 2] (vers bas-droite)
        #Mais peut très bien être par exemple [0.5, 0] (vers droite lentement)
        self.rect.left += self.vitesse[0]
        self.rect.top += self.vitesse[1]

    def Afficher(self, fenetre) -> None:
        #A la fin de chaque frame, on affiche l'individu a sa position en fonction de son rect
        pygame.draw.rect(fenetre, self.couleur, self.rect, width= 0)
#________________________________privé________________________________________________

    def __Decision(self, distance_zone_victoire_x:int, distance_zone_victoire_y:int, cogne) -> tuple:
        #L'individu a comme paramètre sa distance (x et y) au centre de la zone de victoire et s'il touche un obstacle
        donnees:list = [distance_zone_victoire_x, distance_zone_victoire_y, cogne]
        
        #Il va transmettre ces données à ses neurones, qui vont renvoyer un nombre float compris entre -infini et +infini
        #Ce nombre est la nouvelle vitesse de l'individu (en la gardant entre -2 et 2) à chaque décision
        #Donc en fonction des coefficients des neurones de l'individu il aura une certaine vitesse (donc une certaine direction) dans une certaine situation
        #Et seuls les individus ayant "compris" qu'il faut se rapprocher de la zone survivront
        
        activation:float = self.neurone_horizontal.Activation(donnees)
        self.vitesse[0] = activation
        self.vitesse[0] = Clamp(self.vitesse[0], -self.vitesse_max, self.vitesse_max)

        activation:float = self.neurone_vertical.Activation(donnees)
        self.vitesse[1] = activation
        self.vitesse[1] = Clamp(self.vitesse[1], -self.vitesse_max, self.vitesse_max)
        
    def Cloner(self):
        #Renvoie un individu identique à celui-ci
        return Individu(self.neurone_horizontal.Cloner(), self.neurone_vertical.Cloner(), self.couleur)