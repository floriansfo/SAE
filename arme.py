import pygame
import math
from prerequis import obstacle

class Arme:
    def __init__(self, x, y, direction, id =1):
        self.id = id
        #Hitbox de balle
        self.rect = pygame.Rect(0,0,10,10) 
        self.rect.center = (x, y)
        #Coordonnées des balle
        self.posx = float(x)
        self.posy = float(y)
        self.posxori = float(x)
        self.posyori = float(y)
        if self.id == 0:
            self.vitesse = 4
            self.porte = 70
        else:
            self.vitesse = 25 #vitesse des balles
            self.porte = 10000
        self.dist = 0
        # Calcul de la direction de tir
        angle = math.radians(direction)
        self.ux = math.cos(angle) * self.vitesse
        self.uy = -math.sin(angle) * self.vitesse
        #Visuel de la balle
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        if self.id != 0:
            pygame.draw.circle(self.image, (255, 200, 0), (15, 15), 5)  # Dessine une balle jaune

    def deplacer(self, t, joueur = None):
        dx = self.ux * 60 * t
        dy = self.uy * 60 * t
        self.posx += dx
        self.posy += dy
        self.dist += math.hypot(dx, dy)
        if self.id == 0 and joueur is not None:
            self.posxori = float(joueur.rect.centerx)
            self.posyori = float(joueur.rect.centery)
            duree = min(1.0, self.dist / self.porte)
            anglecout = math.degrees(math.atan2(-self.uy, self.ux))
            angleslash = anglecout + 60 - 120 * duree
            r =  45
            slash = math.radians(angleslash)
            cxm = self.posxori + math.cos(slash)*r
            cym = self.posyori - math.sin(slash)*r
            anim = pygame.Surface((160, 160), pygame.SRCALPHA)
            long = 25+int(60*duree)
            larg = max(2, 18-int(16*duree))
            bx = 80-10
            cy2 = 80
            pygame.draw.polygon(anim, (100,200,255), [(bx,cy2-larg-2), (bx+long+4,cy2), (bx,cy2+larg+2)])
            pygame.draw.polygon(anim, (220,220,220), [(bx,cy2-larg), (bx+long,cy2), (bx,cy2+larg)])
            pygame.draw.polygon(anim, (255,255,255), [(bx,cy2-larg//2), (bx+long-5,cy2), (bx,cy2)])
            self.image = pygame.transform.rotate(anim, angleslash)
            self.rect = self.image.get_rect(center=(int(cxm), int(cym)))
        else:
            self.rect.centerx = int(self.posx)
            self.rect.centery = int(self.posy)
    
    def collisionoupas(self, carte, objets):
        if self.dist >= self.porte:
            return True
        # Recupere emplacement des murs
        o = obstacle(self.rect, carte)
        x = self.rect.collidelistall(o)
        if len(x)>0:
            return True
        return False