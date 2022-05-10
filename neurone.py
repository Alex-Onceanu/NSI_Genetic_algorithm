class Neurone:
    #Un Neurone est une classe qui sait juste renvoyer un résultat à partir de données réelles et de coefficients attachés à ces données
    #Chaque Neurone a une liste de "coefficients" ou "poids", qui vont faire varier le résultat que renvoie la fonction Activation
    
    #Via la séléction naturelle, on part d'une population ayant des coefficiens aléatoires (Et qui donc réagissent différemment à certaines situations)
    #Et on séléctionne uniquement les individus ayant des neurones faisant les "bonnes décisions"
    
    #Exemple : avec certains coefficients, un neurone va renvoyer un nombre très faible quand ses données sont élevées (coefficients négatifs)
        #Ou au contraire un nombre très grand dans certaines situations, et seuls ceux remplissant l'objectif du programme survivront
    #Si la donnée est la distance à l'objectif, avec des coefficients négatifs l'individu ira toujours à l'opposé de la zone (et la "fuira") au lieu de s'en rapprocher
        #Car son neurone renverra un nombre négatif (= aller a gauche par exemple) quand le neurone s'approchera de la zone
    
    #Plus rapidement, un neurone c'est juste un résultat à partir de données qu'on lui renvoie ainsi que l'importance que ce neurone-là donne à chaque donnée.
    #La seule fonction importante de cette classe est donc l'Activation
 
    def __init__(self, __coefficients:list) -> None:
        self.coefficients:list = __coefficients
        self.nb_coefficients = len(self.coefficients)

    def Activation(self, donnees_entree:list) -> float:
        #Renvoie un nombre compris entre -infini et +infini, en fonction des donnees_entree et des coefficients du neurone

        #On doit d'abord s'assurer qu'il y a autant de données que de coefficients (cet assert peut être supprimé pour la fin du projet)
        assert len(donnees_entree) == self.nb_coefficients, "Il doit y avoir autant d'informations que de coefficients, len(donnees_entree) = " + str(len(donnees_entree)) + "self.nb_coefficients : " + str(self.nb_coefficients)
        
        #Pour le resultat qui sera le décision qu'aura prise le neurone, on fait simplement une boucle for :
        #On fait la somme de chaque donnée d'entrée multipliée par son coefficient, on trouve donc un résultat dépendant à la fois des données et des coefficients
        #Ainsi les données ayant le plus grand impact sur la décision sont celles ayant les coefficients les plus grands
        rep = 0
        for i in range(self.nb_coefficients):
            rep += donnees_entree[i] * self.coefficients[i]
        
        return rep

    def Cloner(self):
        #Renvoie une copie conforme de ce neurone, donc avec les mêmes coefficients
        return Neurone(self.coefficients.copy())
