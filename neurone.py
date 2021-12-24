from random import uniform
import math

from ModuleUtile import Clamp

class Neurone:
    def __init__(self, __coefficients:list) -> None:
        self.coefficients:list = __coefficients
        self.coefficients.append(uniform(-1,1))
        self.nb_coefficients = len(self.coefficients)

    def Activation(self, donnees_entree:list) -> float:
        assert len(donnees_entree) == self.nb_coefficients-1, "Il doit y avoir autant d'informations que de coefficients, len(donnees_entree) = " + str(len(donnees_entree)) + "self.nb_coefficients : " + str(self.nb_coefficients)
        
        rep = 0
        for i in range(self.nb_coefficients-1):
            rep += donnees_entree[i] * self.coefficients[i]
        rep += self.coefficients[-1]
        #rep = math.tanh(rep)
        rep = Clamp(rep,-1,1)
        return rep

    def Cloner(self):
        tmp = self.coefficients.copy()
        tmp.pop()
        return Neurone(tmp)
