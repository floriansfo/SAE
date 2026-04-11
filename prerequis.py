import pygame
import os 
import math

ZOOM = 180
LARGEURMAP,HAUTEURMAP= 50,50
VITESSEJOUEUR = 10
#Types de cases de la carte
VIDE = 2
MUR = 1
SOL = 0
ASCENCEUR = 3
ETOILE = 4
FLAMME = 5
LIT = 7
#Couleur
NUIT = (15,15,25)
CACHETEXTURE = {}
CACHELUMIERE = {}

#assets
def texture(nom,taille = None, transparente = False):
    cle = (nom, taille, transparente)
    if cle in CACHETEXTURE:
        return CACHETEXTURE[cle]
    chemin = os.path.join("ressource", nom)
    img= pygame.image.load(chemin)
    #Transparence
    if transparente:
        img.set_colorkey((255,255,255))
    #Redimenssionement
    if taille:
        img= pygame.transform.scale(img, taille)
    img = img.convert_alpha()
    CACHETEXTURE[cle] = img
    return img

#Effet Lumiere
def lumiere(rayon):
    if rayon in CACHELUMIERE:
        return CACHELUMIERE[rayon]
    t = int(rayon*2.5)
    #Surface vide pour la transparence
    s = pygame.Surface((t,t),pygame.SRCALPHA)
    #Centre de s
    c = (t//2,t//2)
    #plusieur cercle pour tamiser 
    for i in range(rayon//2,0,-2):
        #calcul opacité
        a = int(100*(i/(rayon//2)))
        if a>0:
            pygame.draw.circle(s,(255,240,200,5),c,i)
    #cone de la lumiere
    longueurcone = rayon
    angless=30  #Degres du cone
    etape = 100 #Puissance dégradé
    for i in range(etape):
        #Distance par rapport au centre
        distance = (i/etape)*longueurcone
        #Largeur du cone
        largeur= int(distance*math.tan(math.radians(angless)))
        posx = c[0]+distance
        posy = c[1]
        #Puissance de la lumiere
        p=60*(1-(i/etape))
        if largeur>0:
            brosse = pygame.Surface((largeur*2,largeur*2), pygame.SRCALPHA)
            pygame.draw.circle(brosse,(255,250,220,int(p)),(largeur,largeur),largeur)
            dist = brosse.get_rect(center=(posx,posy))
            s.blit(brosse,dist,special_flags=pygame.BLEND_RGBA_ADD)
    CACHELUMIERE[rayon] = s
    return s

def angletrace(c, t, f):
    #Calcul rotation pour la fluidité
    d = (t-c+180)%360-180
    return c+d*f

#Collision
def obstacle(rect_joueur,grille):
    obstacle=[]
    #On cherche dans quelle case se trouve joueur
    casex=int(rect_joueur.centerx/ZOOM)
    casey=int(rect_joueur.centery/ZOOM)
    #On cherche un carre de 5x5 autour de lui
    for y in range(max(0,casey-2),min(HAUTEURMAP,casey+3)):
        for x in range(max(0,casex-2),min(LARGEURMAP,casex+3)):
            case = grille[y][x]
            if case == MUR or case == VIDE:
                obstacle.append(pygame.Rect(x*ZOOM,y*ZOOM,ZOOM,ZOOM))
    return obstacle