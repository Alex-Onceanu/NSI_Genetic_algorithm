from random import randint

import pygame

from noeud_file import File
from ModuleUtile import Collision, Distance_rects
from individu import Individu
from resolution import RESOLUTION_X, RESOLUTION_Y


class Monde:
    def __init__(self) -> None:
        self.police_ecriture = pygame.font.SysFont(None,48)
        self.police_chrono = pygame.font.SysFont(None,72)

        self.population = File()
        self.nb_individus_ref = 100
        self.nb_individus = self.nb_individus_ref
        
        for _ in range(self.nb_individus):
            p = Individu(randint(0,100), randint(0,100), randint(0,100), randint(0,100), randint(0,100), randint(1,4), randint(20,60),(randint(0,255),randint(0,255),randint(0,255)))
            self.population.Enfiler(p)

        self.chrono_generation = 0
        self.affichage_chrono = None
        self.nb_gagnants = 0
        self.affichage_gagnants = None
        self.generation = 1
        self.affichage_generation = None
        self.montrer_que_le_meilleur = False
        self.affichage_montrer_que_le_meilleur = None

        self.zone_victoire = pygame.Rect(400, 200, 136,136)

    def Gerer_Evenements(self, evenements:tuple) -> None:
        for evenement in evenements[1]:
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_w:
                self.montrer_que_le_meilleur = not self.montrer_que_le_meilleur

    def Mise_A_Jour(self) -> None:
        gagnants_cette_frame = 0

        self.chrono_generation += 1
        self.affichage_chrono = self.police_chrono.render(str((self.chrono_generation//6)/10),True,(0,0,255))
        self.affichage_gagnants = self.police_ecriture.render("Gagnants : " + str(self.nb_gagnants),True,(0,0,255))
        self.affichage_generation = self.police_ecriture.render("Generation : " + str(self.generation),True,(0,0,255))
        self.affichage_montrer_que_le_meilleur = self.police_ecriture.render("Montrer que le meilleur",True,(255,0,0))

        for _ in range(self.nb_individus):
            individu = self.population.Defiler()
            individu.Mise_A_Jour()
            if not individu.mort:
                if Collision(individu.rect, self.zone_victoire):
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

        fenetre.blit(self.affichage_gagnants,(RESOLUTION_X()//24, 36))
        fenetre.blit(self.affichage_chrono,(RESOLUTION_X()//2-36, 36))
        fenetre.blit(self.affichage_generation, (RESOLUTION_X()*7/9, 36))
        if self.montrer_que_le_meilleur:
            fenetre.blit(self.affichage_montrer_que_le_meilleur, (RESOLUTION_X()//24, RESOLUTION_Y()-36))

    def Nouvelle_Generation(self) -> None:
        l = []
        while not self.population.est_vide():
            l.append(self.population.Defiler())
            
        l.sort(key=self.Distance_a_zone_victoire)

        if self.montrer_que_le_meilleur:
            self.population.Enfiler(l[0].Cloner())

        while len(self.population) < self.nb_individus_ref:
            for male in range(0,6):
                for femelle in range(male,20):
                    nouveau = Croisement_individus(l[male], l[femelle])
                    if self.montrer_que_le_meilleur :
                        nouveau.rect.width = 0
                    self.population.Enfiler(nouveau)

        self.nb_individus = self.nb_individus_ref
        self.chrono_generation = 0
        self.generation += 1

    def Distance_a_zone_victoire(self, a):
        return Distance_rects(a.rect, self.zone_victoire)

def Croisement_individus(a:Individu, b:Individu) -> Individu:
    #On croise chaque chromosome des 2 individus pour en creer un nouveau

    nouv_p_gauche = Croisement_chromosomes(a.p_gauche, b.p_gauche)
    nouv_p_droite = Croisement_chromosomes(a.p_droite, b.p_droite)
    nouv_p_haut = Croisement_chromosomes(a.p_haut, b.p_haut)
    nouv_p_bas = Croisement_chromosomes(a.p_bas, b.p_bas)
    nouv_p_stop = Croisement_chromosomes(a.p_stop, b.p_stop)
    nouv_vitesse_max = Croisement_chromosomes(a.vitesse_max, b.vitesse_max)
    nouv_taux_decision = Croisement_chromosomes(a.taux_decision, b.taux_decision)
    if nouv_taux_decision > 60 : nouv_taux_decision = 60
    if nouv_taux_decision < 20 : nouv_taux_decision = 20
    nouv_couleur = ((a.couleur[0] + b.couleur[0]) // 2, (a.couleur[1] + b.couleur[1]) // 2, (a.couleur[2] + b.couleur[2]) // 2)

    return Individu(nouv_p_gauche, nouv_p_droite, nouv_p_haut, nouv_p_bas, nouv_p_stop, nouv_vitesse_max, nouv_taux_decision, nouv_couleur)

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
