from random import randint
from random import uniform

import pygame
from neurone import Neurone

from noeud_file import File
from ModuleUtile import Collision, Distance_rects
from individu import Individu
from resolution import RESOLUTION_X, RESOLUTION_Y


class Monde:
    def __init__(self) -> None:
        self.police_ecriture = pygame.font.SysFont(None,48)
        self.police_chrono = pygame.font.SysFont(None,72)

        self.nb_individus_ref = 1000
        self.nb_individus = self.nb_individus_ref

        #Création de la file de population dans la fonction __Reset()    
        self.__Reset()
        
        self.affichage_chrono = None
        self.nb_gagnants = 0
        self.affichage_gagnants = None
        self.affichage_generation = None
        self.montrer_que_le_meilleur:bool = False
        self.affichage_montrer_que_le_meilleur = self.police_ecriture.render("Montrer que le meilleur",True,(255,0,0))

        self.zone_victoire = pygame.Rect(randint(0,RESOLUTION_X()-236), randint(0,RESOLUTION_Y()-236), 236,236)
        self.suivre_curseur = False

    def Gerer_Evenements(self, evenements:tuple) -> None:
        for evenement in evenements[1]:
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_w:
                self.montrer_que_le_meilleur = not self.montrer_que_le_meilleur
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_r:
                self.suivre_curseur = not self.suivre_curseur
                self.zone_victoire.center = pygame.mouse.get_pos()

    def Mise_A_Jour(self) -> None:
        if self.suivre_curseur:
            self.zone_victoire.center = pygame.mouse.get_pos()

        gagnants_cette_frame = 0
        self.chrono_generation += 1
        self.__Mise_A_Jour_Ecriture()

        for _ in range(self.nb_individus):
            individu = self.population.Defiler()
            touche_zone_victoire = Collision(individu.rect, self.zone_victoire)
            individu.Mise_A_Jour(self.zone_victoire.centerx - individu.rect.centerx, self.zone_victoire.centery - individu.rect.centery, touche_zone_victoire)
            if not individu.mort:
                if touche_zone_victoire:
                    gagnants_cette_frame += 1
                self.population.Enfiler(individu)
        
        self.nb_gagnants = gagnants_cette_frame
        self.nb_individus = len(self.population)

    def Afficher(self, fenetre) -> None:
        fenetre.fill((255,255,255))
        pygame.draw.rect(fenetre, (205,255,185), self.zone_victoire, width=0)

        for _ in range(self.nb_individus):
            individu = self.population.Defiler()
            individu.Afficher(fenetre)
            self.population.Enfiler(individu)
        self.__Affichage_Ecriture(fenetre)

    def Nouvelle_Generation(self) -> None:
        l = []
        while not self.population.est_vide():
            l.append(self.population.Defiler())
        self.population = File()
        l.sort(key=self.__Distance_a_zone_victoire)

        if self.montrer_que_le_meilleur:
            self.population.Enfiler(l[0])
            self.nb_individus = 1

        else:
            if self.nb_individus == 1:
                return self.__Reset()
            nb_survivants = self.nb_gagnants if self.nb_gagnants >= 10 else self.nb_individus_ref//100
            while len(self.population) < self.nb_individus_ref:
                for male in range(0,nb_survivants):
                    if len(self.population) >= self.nb_individus_ref: break
                    for femelle in range(male,nb_survivants):
                        if len(self.population) >= self.nb_individus_ref: break
                        nouveau = Croisement_individus(l[male], l[femelle])
                        self.population.Enfiler(nouveau)
            self.nb_individus = self.nb_individus_ref

        self.chrono_generation = 0
        self.generation += 1

#__________________________________privé_______________________________________________________________________________

    def __Reset(self) -> None:
        self.population = File()
        NB_COEFFICIENTS_NEURONE = 7
        for _ in range(self.nb_individus_ref):
            neurone_hor = Neurone([uniform(-1,1) for _ in range(NB_COEFFICIENTS_NEURONE)])
            neurone_ver = Neurone([uniform(-1,1) for _ in range(NB_COEFFICIENTS_NEURONE)])
        
            p = Individu(neurone_hor, neurone_ver, (randint(0,255),randint(0,255),randint(0,255)))
            self.population.Enfiler(p)
        self.generation = 1
        self.chrono_generation = 0

    def __Mise_A_Jour_Ecriture(self) -> None:
        self.affichage_chrono = self.police_chrono.render(str((self.chrono_generation//6)/10),True,(0,0,255))
        self.affichage_gagnants = self.police_ecriture.render("Gagnants : " + str(self.nb_gagnants),True,(0,0,255))
        self.affichage_generation = self.police_ecriture.render("Generation : " + str(self.generation),True,(0,0,255))

    def __Affichage_Ecriture(self, fenetre) -> None:
        fenetre.blit(self.affichage_generation, (RESOLUTION_X()*7/9, 36))
        fenetre.blit(self.affichage_gagnants,(RESOLUTION_X()//24, 36))
        
        
        if self.montrer_que_le_meilleur:
            fenetre.blit(self.affichage_montrer_que_le_meilleur, (RESOLUTION_X()//24, RESOLUTION_Y()-36))
        else:
            fenetre.blit(self.affichage_chrono,(RESOLUTION_X()//2-36, 36))

    def __Distance_a_zone_victoire(self, a):
        return Distance_rects(a.rect, self.zone_victoire)

#_________________________________________sortie_de_classe_____________________________________________________________________________________


#A faire : les coefficients pris de chaque neurone de chaque individu sont coupés a partir de la moitié.
#Faire que ça coupe à un endroit aléatoire, et que donc ça prenne un nombre aléatoire de coeffs de chaque neurone.
def Croisement_individus(a:Individu, b:Individu) -> Individu:
    neurones_b = [b.neurone_horizontal, b.neurone_vertical]
    neurones_a = [a.neurone_horizontal, a.neurone_vertical]
    nouveaux_neurones = []
    for i in range(len(neurones_a)):
        n_a = neurones_a[i]
        n_b = neurones_b[i]
        nouv_coefficients = []
        for coef in range(n_a.nb_coefficients -1 ):
            if coef <= n_a.nb_coefficients // 2:
                nouv_coefficients.append(n_a.coefficients[coef])
            else:
                nouv_coefficients.append(n_b.coefficients[coef])
        nouveaux_neurones.append(Neurone(nouv_coefficients))

    nouv_couleur = ((a.couleur[0] + b.couleur[0]) // 2, (a.couleur[1] + b.couleur[1]) // 2, (a.couleur[2] + b.couleur[2]) // 2)

    return Individu(nouveaux_neurones[0], nouveaux_neurones[1], nouv_couleur)

def Croisement_chromosomes(a, b):
    if randint(0,1) == 1: return Croisement_chromosomes_v2(a, b)

    #On croise les bits des deux individus en coupant les deux octets a un endroit aleatoire
    #On prend la partie gauche du 1er chromosome et la partie droite du 2eme
    bit_coupure = randint(0,8)
    calque_a = 2**bit_coupure -1

    calque_b = calque_a ^ 0b1111111
    #calque_b est l'opposé binaire de calque_a, pour le trouver on utilise XOR avec 11111111

    #Si bit coupure vaut 3 alors calque_a vaut 11100000 et calque_b 00011111
    #Le calque_a est un nombre "bit_coupure" de bits 1 tout a gauche, calque_b tout a droite

    a = a & calque_a
    b = b & calque_b
    return a | b

def Croisement_chromosomes_v2(a, b):
    #On prend 2 bits de chaque chromosome
    #Pour ça il nous faut 2 calques, 11001100 pour a et 00110011 pour b
    calque_a = 0b11001100
    calque_b = 0b00110011

    a = a & calque_a
    b = b & calque_b

    return a | b
