import pygame
from prerequis import HAUTEURMAP, LARGEURMAP, VIDE, SOL, MUR, ASCENCEUR, ETOILE, FLAMME

LIT = 7
BOUTIQUE = 8

def generer_vaisseau():
    grille = [[ETOILE for i in range(LARGEURMAP)]for k in range(HAUTEURMAP)]
    salle = []

    #Dessine sol
    largeur = 13
    hauteur = 14
    startx = (LARGEURMAP - largeur) // 2
    starty = (HAUTEURMAP - hauteur) // 3
    finx = startx + largeur
    finy = starty + hauteur
    centrex = startx+(largeur // 2)

    #Pointe du vaisseau
    for y in range(starty, starty+7):
        demi = y-starty
        for x in range(centrex-demi, centrex+demi+1):
                grille[y][x] = SOL
    #Rectangle  du vaisseau
    for y in range(starty+7, finy):
        for x in range(startx, finx):
            grille[y][x] = SOL
    #Ascenceur
    ascy = starty+4
    grille[ascy][centrex] = ASCENCEUR
    #Spawn
    spawny = starty + 11
    grille[spawny][centrex] = SOL
    spawn_pos = (centrex, ascy)
    #Lit
    lity,litx = starty+9, centrex-3
    grille[lity][litx] = LIT
    #Boutique
    boutiquey,boutiquex = starty+9, centrex+3
    grille[boutiquey][boutiquex] = BOUTIQUE
    #Dessine les murs intérieurs
    grillefinale = [row[:] for row in grille]
    INTERIEUR = {SOL, ASCENCEUR, LIT, BOUTIQUE}
    for y in range(1,HAUTEURMAP-1):
        for x in range(1,LARGEURMAP-1):
            #Si on est dans le vide
            if grille[y][x] == ETOILE:
                if any(grille[y+d][x+e]in INTERIEUR for d in (-1,0,1) for e in (-1,0,1)):
                    grillefinale[y][x] = MUR

    #Dessine Flamme
    for x in range(startx+2, finx-2):
        for yflamme in range(finy+1, min(finy+4,HAUTEURMAP)):
                grillefinale[yflamme][x] = FLAMME
    return grillefinale, salle, spawn_pos

