import pygame
import math
from prerequis import obstacle

class Arme:
    def __init__(self, x, y, direction):
        #Hitbox de balle
        self.rect = pygame.Rect(0,0,10,10) 
        self.rect.center = (x, y)
        #Coordonnées des balle
        self.posx = float(x)
        self.posy = float(y)
        self.vitesse = 25 #vitesse des balles
        #Orientation balle
        angleballe = math.radians(-direction)
        self.dx = math.cos(angleballe)
        self.dy = math.sin(angleballe)
        # Calcul de la direction de tir
        angle = math.radians(direction)
        self.ux = math.cos(angle) * self.vitesse
        self.uy = -math.sin(angle) * self.vitesse
        #Visuel de la balle
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 200, 0), (5, 5), 5)  # Dessine une balle jaune

    def deplacer(self, t):
        self.posx += self.ux*60*t
        self.posy += self.uy*60*t
        self.rect.centerx = int(self.posx)
        self.rect.centery = int(self.posy)
    
    def collisionoupas(self, carte, objets):
        # Recupere emplacement des murs
        o = obstacle(self.rect, carte)
        # Vérifie la collision avec les objets
        for obj in objets:
            typee=getattr(obj, "type", "")
            if typee == "meuble":
                if self.rect.colliderect(obj.hitbox):
                    return obj
        # Vérifie la collision avec les murs
        for mur in o:
            if self.rect.colliderect(mur):
                return "mur"
        return None