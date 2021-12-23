class Noeud:
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
        tmp = Noeud(val, None)

        if self.est_vide():
            self.tete = tmp
        else:
            self.queue.suivant = tmp

        self.queue = tmp

    def Defiler(self):
        if self.est_vide():
            return None

        tmp = self.tete.contenu
        self.tete = self.tete.suivant

        if self.est_vide():
            self.queue = None

        return tmp

    def __len__(self) -> int:
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
