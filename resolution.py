#Constantes de la résolution de la fenêtre du programme
#Peut être pratique d'y avoir accès depuis n'importe où

def RESOLUTION_X() -> int:
    return 1366

def RESOLUTION_Y() -> int:
    return 768

def RESOLUTION() -> tuple:
    return RESOLUTION_X(), RESOLUTION_Y()