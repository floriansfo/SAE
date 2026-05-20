import pygame
import math

#Couleur
NUIT = (10, 10, 20)
NUIT_ALPHA = 245  #cacher la map
CONE_ANGLE  = 30
CONE_PORTEE = 480
RONDPORTEE = 150
RONDCOUCHE = 40

def cone(portee, angle, couleur, couche = 80):
    #On calcul la porté de la lumiere
    taille = portee*2
    lumiere = pygame.Surface((taille,taille), pygame.SRCALPHA)
    #On dit qu'il demarre au niveau du joueur
    ix = iy = portee
    rayon = math.radians(angle)
    r,g,b =couleur
    #Donne le cote arrondi au cone
    rond = max(32, int(angle*3))
    for i in range(couche, 0, -1):
        dist = i/couche #De 1 (bout du cone) a 0 (proche du joueur)
        rayoncouche = int(portee*dist)
        #Degrade plus on est proche du joueur alors alpha = 255 sinon 0
        alpha = min(255, int(255*(1-(dist**0.5))*2))
        #Cone de rayon
        points= [(ix,iy)]
        for k in range(rond+1):
            #Angle en degres
            anglee = -rayon+(2*rayon*k/rond)
            kx = ix + math.cos(anglee)*rayoncouche
            ky = iy + math.sin(anglee)*rayoncouche
            points.append((kx,ky))
        if len(points) >= 3:
            pygame.draw.polygon(lumiere, (r, g, b, alpha), points)
    return lumiere

def rond(portee, couche=RONDCOUCHE):
    taille = portee*2
    surface = pygame.Surface((taille, taille), pygame.SRCALPHA)
    cx = cy = portee
    for i in range(couche, 0, -1):
        dist = i/couche
        rayoncouche = int(portee*dist)
        alpha = int(220*(1-dist**1.5))
        pygame.draw.circle(surface, (255, 220, 150, alpha), (cx, cy), rayoncouche)
    return surface

class Lumiere:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        #Calcul le cone
        self.cone = cone(CONE_PORTEE, CONE_ANGLE, (255, 240, 200))
        self.rond = rond(RONDPORTEE)
        self.angle = None
        self.rotation = None
        self.masque = pygame.Surface((self.largeur,self.hauteur), pygame.SRCALPHA)

    def redimenssione(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.masque = pygame.Surface((self.largeur,self.hauteur), pygame.SRCALPHA)

    def conerota(self, anglejoueur):
        #Pivote le cone vers l'endroit ou regarde le joueur
        anglerota = int(anglejoueur)%360
        if anglerota != self.angle:
            self.rotation = pygame.transform.rotate(self.cone, anglerota)
            self.angle = anglerota
        return self.rotation
    
    def appliquer(self, ecran, joueur, joueursup, camera_x, camera_y, niveau_actuel, mode_combat=False):
        #Si mode combat alors aps de masque noir
        if mode_combat:
            return
        ecranl, ecranh = ecran.get_size()
        if ecranl != self.largeur or ecranh != self.hauteur:
            self.redimenssione(ecranl, ecranh)
        #Active lampe apres generation map
        self.masque.fill((*NUIT, NUIT_ALPHA))
        cx = int(joueur.rect.centerx+camera_x)
        cy = int(joueur.rect.centery+camera_y)
        rectrond = self.rond.get_rect(center=(cx,cy))
        self.masque.blit(self.rond, rectrond, special_flags=pygame.BLEND_RGBA_SUB)
        if getattr(joueur, "lumiereallumee", False):
            cone = self.conerota(joueur.angleactuel)
            rectcone = cone.get_rect(center=(cx,cy))
            self.masque.blit(cone, rectcone, special_flags=pygame.BLEND_RGBA_SUB)
        if joueursup:
            for idjoueur, autre in joueursup.items():
                if getattr(autre, "etage", 1) == niveau_actuel and not getattr(autre, "mort", False):
                    ax = int(autre.rect.centerx+camera_x)
                    ay = int(autre.rect.centery+camera_y)
                    if -200<ax<self.largeur+200 and -200<ay<self.hauteur+200:
                        rectautre = self.rond.get_rect(center=(ax,ay))
                        self.masque.blit(self.rond, rectautre, special_flags=pygame.BLEND_RGBA_SUB)
                        if getattr(autre, "lumiere", False):
                            coneautre = self.conerota(getattr(autre, "angleactuel", autre.angle-90))
                            rectcone = coneautre.get_rect(center=(ax,ay))
                            self.masque.blit(coneautre, rectcone, special_flags=pygame.BLEND_RGBA_SUB)
        ecran.blit(self.masque, (0,0))