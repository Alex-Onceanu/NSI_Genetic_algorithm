#Classes Noeud et File vues en cours, permettent de gérer les individus en les plaçant tous dans une File

class Noeud:
    #Chaque Noeud est un individu qui connait l'emplacement mémoire de l'individu suivant
    def __init__(self, contenu_, suivant_) -> None:
        self.contenu = contenu_
        self.suivant =  suivant_

class File:
    def __init__(self) -> None:
        self.tete = None
        self.queue = None
    
    def est_vide(self) -> bool:
        return self.tete is None

    def Enfiler(self, val) -> None:
        #Ajoute un élément val au bout de la file
        tmp = Noeud(val, None)

        if self.est_vide():
            self.tete = tmp
        else:
            self.queue.suivant = tmp

        self.queue = tmp

    def Defiler(self):
        #On a uniquement accès au premier élément de la liste, le renvoie et l'enlève de la file
        if self.est_vide():
            return None

        tmp = self.tete.contenu
        self.tete = self.tete.suivant

        if self.est_vide():
            self.queue = None

        return tmp

    def __len__(self) -> int:
        #Compte le nombre d'éléments de la file
        AUX = File()
        compt = 0
        while not self.est_vide():
            tmp = self.Defiler()
            AUX.Enfiler(tmp)
            compt += 1
        while not AUX.est_vide():
            tmp = AUX.Defiler()
            self.Enfiler(tmp)
        return compt
