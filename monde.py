from random import randint
from random import uniform

import pygame
from neurone import Neurone
from niveaux import ObtenirNiveaux

from noeud_file import File
from ModuleUtile import Collision, Distance_rects
from individu import Individu
from resolution import RESOLUTION_X, RESOLUTION_Y


class Monde:
    #La classe Monde met en lien tous les différents éléments du jeu et les gère : la file d'individus, les zones de texte, la zone de victoire etc
    def __init__(self) -> None:
        self.nb_individus_ref = 200
        self.nb_individus = self.nb_individus_ref

        #Polices d'écriture, utilisées pour afficher des textes à l'écran
        self.police_ecriture = pygame.font.SysFont(None,48)
        self.police_chrono = pygame.font.SysFont(None,72)
        
        #la fonction ObtenirNiveaux() renvoie une liste de Niveaux, contenant la zone et les obstacles a utiliser
        #self.obstacles est une liste de pygame.Rect, où chaque Rect est un obstacle, on pourra donc itérer dans cette liste pour afficher chaque obstacle
        self.zone_victoire = ObtenirNiveaux()[0].zone_victoire
        self.obstacles = ObtenirNiveaux()[0].obstacles
        #Numero (index de la liste d'ObtenirNiveaux()) du niveau actuel
        self.id_niveau_actuel = 0

        #Création de la file de population dans la fonction __Reset()
        #Le programme contient une population d'Individus (voir classe Individu) qui sont gérés depuis le Monde
        #La population est une File d'Individus (voir classe File), et pour itérer on défile un individu, puis on le renfile à la fin de la file
        self.__Reset()
        
        #Les attributs commençant par "affichage" sont des pygame.surface qui sont des textes
        #Ils sont affichés à l'écran dans la fonction self.__Affichage_Ecriture()
        self.affichage_chrono = None
        self.nb_gagnants:int = 0
        self.affichage_gagnants = None
        self.affichage_generation = None
        self.montrer_que_le_meilleur:bool = False
        self.affichage_montrer_que_le_meilleur = self.police_ecriture.render("Montrer que le meilleur",True,(255,0,0))


        #Est ce que la zone verte de victoire doit suivre la souris
        self.suivre_curseur = False

    def Gerer_Evenements(self, evenements:list) -> None:
        #Gestion des appuis de touches et autres interactions avec l'utilisateur

        #On itère dans la liste d'évenements donnés par pygame
        for evenement in evenements:
            #Si on reconnait une certaine touche, on active un certain mode
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_w:
                self.montrer_que_le_meilleur = not self.montrer_que_le_meilleur
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_r:
                self.suivre_curseur = not self.suivre_curseur
                self.zone_victoire.center = pygame.mouse.get_pos()

    def Mise_A_Jour(self) -> None:
        #Ce qui est différent d'une frame à l'autre; toutes les actualisations se font ici

        #Si le mode "suivre curseur" est activé la zone de victoire va a l'emplacement de la souris
        if self.suivre_curseur:
            self.zone_victoire.center = pygame.mouse.get_pos()

        #gagnants_cette_frame va servir a compter le nombre d'individus dans la zone
        gagnants_cette_frame = 0
        self.chrono_generation += 1

        #On itère dans la file d'individus pour appeler leur propre fonction Mise_A_Jour
        #Pour itérer à travers une file, on Defile chaque élément (chaque individu) un à un, on lance sa fonction Mise_A_Jour puis on le fait revenir à la fin de la file
        for _ in range(self.nb_individus):
            individu = self.population.Defiler()

            #On verifie ici si l'individu touche un obstacle
            cogne = self.__Gerer_Collisions(individu)
            individu.Mise_A_Jour(self.zone_victoire.centerx - individu.rect.centerx, self.zone_victoire.centery - individu.rect.centery, cogne)
            
            #Si l'individu en question est mort on ne l'ajoute pas a la file, il sera récupéré par le GC a la frame suivante
            if not individu.mort:
                #Si l'individu est dans la zone de victoire, on incrémente le nombre de gagnants
                if Collision(individu.rect, self.zone_victoire):
                    gagnants_cette_frame += 1
                self.population.Enfiler(individu)
        
        self.nb_gagnants = gagnants_cette_frame
        self.nb_individus = len(self.population)

        #Suite de la fonction pour mettre à jour les textes, tout ça est séparé dans une fonction annexe pour pas polluer 
        self.__Mise_A_Jour_Ecriture()

    def Afficher(self, fenetre) -> None:
        #Une fois que tous les calculs ont été faits dans la fonction Mise_A_Jour, on affiche tous les éléments du jeu
        
        #On commence par effacer l'écran de la frame précédante en coloriant l'écran de blanc
        fenetre.fill((255,255,255))

        #Afficher la zone de victoire
        pygame.draw.rect(fenetre, (205,255,185), self.zone_victoire, width=0)

        #On itère à travers la file d'individus pour afficher chacun d'entre eux
        #Note : chaque individu sait lui-même se dessiner, on a donc juste a appeler leur propre fonction Afficher
        for _ in range(self.nb_individus):
            individu = self.population.Defiler()
            individu.Afficher(fenetre)
            self.population.Enfiler(individu)

        #On affiche tous les obstacles
        for o in self.obstacles:
            pygame.draw.rect(fenetre, (0,0,255), o, width=0)

        #Suite de la fonction pour afficher les textes, tout ça est séparé dans une fonction annexe pour pas polluer 
        self.__Affichage_Ecriture(fenetre)

    def Nouvelle_Generation(self) -> None:
        #A la fin de chaque génération, il faut déterminer qui survit et qui meurt.
        #Selection naturelle : les bons survivent et se reproduisent entre eux, les mauvais meurent.
        #A partir des survivants de la génération précédente, on crée une nouvelle génération plus efficace

        #On va mettre tous les individus dans cette liste, comme ça on peut les trier en fonction de qui est le plus proche de la zone de victoire
        l = []
        while not self.population.est_vide():
            l.append(self.population.Defiler())
        self.population = File()

        #On a déplacé l'ensemble de la population dans la liste l, on la trie
        #Les premiers de la liste seront les plus proches de la zone de victoire
        l.sort(key=self.__Distance_a_zone_victoire)

        #Si le mode "montrer que le meilleur" est activé, on ne montre qu'un copie du meilleur, tous les autres meurent
        if self.montrer_que_le_meilleur:
            self.population.Enfiler(l[0])
            if self.nb_individus == 1: return
            print(l[0].neurone_vertical.coefficients)
            print(l[0].neurone_horizontal.coefficients)
            self.nb_individus = 1

        else:
            if self.nb_individus == 1:
                #Si le mode "montrer que le meilleur" est désactivé après avoir été activé, on réinitialise la population.
                return self.__Reset()

            #S'il y a plus de 19 individus ayant fini la génération dans la zone de victoire, on ne garde qu'eux et on tue tous les autres
            #Si c'est pas le cas, on prend les 19 plus proches du centre de la zone
            #Pourquoi 19 ? parce que 19 + 18 + 17 + 16 + ... + 1 = 204 donc presque 200, et on veut 200 individus 
            nb_survivants = self.nb_gagnants if self.nb_gagnants >= 19 else 19

            while len(self.population) < self.nb_individus_ref:
                #Les survivants se reproduisent jusqu'à ce que la population arrive à 1000 et que donc on ait une nouvelle génération complète
                
                for male in range(0,nb_survivants):
                    #On arrête la boucle si on a déja atteint le nombre d'individus voulu
                    if len(self.population) >= self.nb_individus_ref: break

                    for femelle in range(male,nb_survivants):
                        #On arrête la boucle si on a déja atteint le nombre d'individus voulu
                        if len(self.population) >= self.nb_individus_ref: break

                        #Chaque survivant se reproduit avec les survivants plus "bas dans la liste" que lui
                        #Donc le meilleur se reproduit avec tout le monde, le 2eme avec tout le monde sauf le premier, etc
                        nouveau = Croisement_individus(l[male], l[femelle])

                        #On ajoute à la prochaine génération le croisement entre ces deux survivants
                        self.population.Enfiler(nouveau)
            self.nb_individus = self.nb_individus_ref

        self.chrono_generation = 0
        self.generation += 1

        #Si 80% des individus sont dans la zone, on passe au niveau suivant en incrémentant id_niveau_actuel
        if self.nb_gagnants >= self.nb_individus_ref * 4/5:
            if self.id_niveau_actuel < len(ObtenirNiveaux()) - 1:
                self.id_niveau_actuel += 1
                self.__Reset()
            else:
                #Ce else s'active si on est arrivés au dernier niveau, auquel cas le mode "montrer que le meilleur" est activé
                self.id_niveau_actuel = len(ObtenirNiveaux())-1 
                self.population = File()
                self.population.Enfiler(l[0])
                self.nb_individus = 1
                self.montrer_que_le_meilleur = True

#__________________________________privé_______________________________________________________________________________

    def __Reset(self) -> None:
        #La population est réinitialisée, tout redevient aléatoire comme à la génération 1
        self.population = File()

        #Car chaque neurone prend en compte deux paramètres, donc a deux coefficients
        NB_COEFFICIENTS_NEURONE = 3
        for _ in range(self.nb_individus_ref):
            #On crée deux neurones avec des coefficients absolument aléatoires
            neurone_hor = Neurone([uniform(-1,1) for _ in range(NB_COEFFICIENTS_NEURONE)])
            neurone_ver = Neurone([uniform(-1,1) for _ in range(NB_COEFFICIENTS_NEURONE)])
        
            #On ajoute à la population ce nouvel individu avec une couleur aléatoire
            p = Individu(neurone_hor, neurone_ver, (randint(0,255),randint(0,255),randint(0,255)))
            self.population.Enfiler(p)

        self.generation = 1
        self.chrono_generation = 0

        #Les obstacles et la zone sont mis à jour en fonction de l'index du niveau actuel
        self.zone_victoire = ObtenirNiveaux()[self.id_niveau_actuel].zone_victoire
        self.obstacles = ObtenirNiveaux()[self.id_niveau_actuel].obstacles

    def __Mise_A_Jour_Ecriture(self) -> None:
        #Suite de la fonction mise à jour destinée uniquement pour les textes
        self.affichage_chrono = self.police_chrono.render(str((self.chrono_generation//6)/10),True,(0,0,255))
        self.affichage_gagnants = self.police_ecriture.render("Gagnants : " + str(self.nb_gagnants),True,(0,0,255))
        self.affichage_generation = self.police_ecriture.render("Generation : " + str(self.generation),True,(0,0,255))

    def __Affichage_Ecriture(self, fenetre) -> None:
        #Fonction qui affiche les textes du jeu, j'ai préféré séparer ça dans une nouvelle fonction
        fenetre.blit(self.affichage_generation, (RESOLUTION_X()*7/9, 36))
        fenetre.blit(self.affichage_gagnants,(RESOLUTION_X()//24, 36))
        
        if self.montrer_que_le_meilleur:
            fenetre.blit(self.affichage_montrer_que_le_meilleur, (RESOLUTION_X()//24, RESOLUTION_Y()-36))
        else:
            fenetre.blit(self.affichage_chrono,(RESOLUTION_X()//2-36, 36))

    def __Gerer_Collisions(self, individu) -> bool:
        #Si l'individu touche un obstacle on l'empêche d'avancer et on renvoie True

        #Pour chaque individu on vérifie s'il touche un obstacle
        #cogne vaut True si l'individu est en collision avec au moins un obstacle
        cogne = False
        for o in self.obstacles:
            if Collision(individu.rect, o):
                #Chaque individu a un attribut position_frame_precedente qui est une sauvegarde de son ancienne position
                #Il suffit de le faire revenir à cette ancienne position en cas de collision pour "l'arrêter" 
                individu.rect.left = individu.position_frame_precedente[0]
                individu.rect.top = individu.position_frame_precedente[1]
                cogne = True
                break
        return cogne

    def __Distance_a_zone_victoire(self, a):
        #Fonction utilisée en tant que key pour le tri des individus
        return Distance_rects(a.rect, self.zone_victoire)

#_________________________________________sortie_de_classe_____________________________________________________________

def Croisement_individus(a:Individu, b:Individu) -> Individu:
    #On veut obtenir un nouvel individu à partir de deux parents
    #L'enfant doit plus ou moins ressembler à ses parents, sans pour autant en être identique
    #Comme ça il y a de la diversité dans la population, tout en continuant de s'améliorer
    #Pour croiser deux individus, on fait le croisement des coefficients de leurs neurones
    #Donc on prend quelques coefficients de l'individu a, quelques uns du b, et on obient un neurone qui fera __presque__ les même decisions que les parents

    #On liste tous les neurones de chaque individu
    neurones_b = [b.neurone_horizontal, b.neurone_vertical]
    neurones_a = [a.neurone_horizontal, a.neurone_vertical]
    #Cette liste contiendra les neurones du nouvel individu
    nouveaux_neurones = []

    #On prend un nombre aléatoire de coefficients de chaque neurone des individus
    coupure = randint(0, neurones_a[0].nb_coefficients)
    for i in range(len(neurones_a)):
        #On prend chaque neurone des 2 individus à part
        n_a = neurones_a[i]
        n_b = neurones_b[i]
        nouv_coefficients = []
        for coef in range(n_a.nb_coefficients):
            #On prend chaque coefficient des deux neurones
            if coef <= coupure:
                nouv_coefficients.append(n_a.coefficients[coef])
            else:
                nouv_coefficients.append(n_b.coefficients[coef])
        #On a obtenu une liste nouv_coefficients qui contient un mix des coeffs des neurones des 2 individus.
        nouveaux_neurones.append(Neurone(nouv_coefficients))

    #La couleur du nouvel individu sera le moyenne des couleurs de ses parents.
    nouv_couleur = ((a.couleur[0] + b.couleur[0]) // 2, (a.couleur[1] + b.couleur[1]) // 2, (a.couleur[2] + b.couleur[2]) // 2)

    return Individu(nouveaux_neurones[0], nouveaux_neurones[1], nouv_couleur)
