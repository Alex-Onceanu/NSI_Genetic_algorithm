from typing import List
from pygame import Rect

class Niveau:
    def __init__(self, __zone_victoire:Rect, __obstacles:List[Rect]) -> None:
        self.zone_victoire = __zone_victoire
        self.obstacles = __obstacles

def ObtenirNiveaux() -> List[Niveau]:
    return [
        Niveau(Rect(800, 200, 128, 128), []),
        Niveau(Rect(864, 264, 100, 100), [Rect(600,200,10,400), Rect(800,300,10,400)]),
        Niveau(Rect(700, 500, 100, 100), [Rect(685,500,15,100), Rect(685,485,115,15), Rect(685,600,115,15)]),
        Niveau(Rect(1100, 500, 100, 100), [Rect(400,485,800,15), Rect(400,600,800,15), Rect(1200,485,15,130), Rect(400,-10000,15,10485), Rect(400,600,15,10485)]),
        Niveau(Rect(800, 200, 128, 128), [Rect(500,40,10,680), Rect(460,650,10,10000), Rect(460,-9900,10,10000), Rect(-500,90,960,10), Rect(-500,640,970,10)]),
        Niveau(Rect(800, 200, 128, 128), []),
    ]