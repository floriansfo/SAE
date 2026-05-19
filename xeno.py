import pygame
import random
import assets
from monstre import Monstre, move, Direction
from prerequis import dist_mj



class Xeno(Monstre):
    def __init__(self, x, y,):
        super().__init__(x, y, 3, 100)
        self.degats= 20
        self.cible=None
        self.direction= Direction.face
        #animation
        self.animation=0
        self.time=0
        self.vitesseanim=5

    
    def deplacement(self, t, joueur_x=None, joueur_y = None):
        kx= self.pos_x * self.speed*60*t
        ky = self.pos_y * self.speed*60*t
        if self.cible is not None:
            #Direction vers sa cible
            dx = self.cible.rect.centerx -self.rect.centerx
            dy = self.cible.rect.centery - self.rect.centery
            #Distance avec le joueur calcul
            distance = dist_mj(self.cible.rect, self.rect)
            #maj de l'affichage en fct de la direction
            self.direction= Direction.mouvement(dx, dy)
            if self.bloque and distance>0:
                kx = (-dy/distance) *self.speed*60*t
                ky = (dx/distance) *self.speed*60*t
                return (kx, ky)
            #Lorsque le joueur est proche
            if distance >0:
                kx = (dx/distance) *self.speed*60*t
                ky = (dy/distance) *self.speed*60*t
                return (kx, ky)
        #sinon mouvements aléatoires 
        if(random.random()<0.02):
            self.pos_x= random.choice(move)
            self.pos_y= random.choice(move)
            if(self.pos_x!=0 or self.pos_y !=0):
                self.direction= Direction.mouvement(self.pos_x, self.pos_y)
    
        kx= self.pos_x*self.speed*60*t
        ky= self.pos_y * self.speed*60*t  
        return (kx, ky)
    
    def comportement(self,t, joueurs) :
        #recherche du joueur
        if not self.cible:
            for joueur in joueurs:
                if dist_mj(self.rect, joueur.rect)<600:
                    self.cible =joueur
        else:
            #puis part si trop loin
            if dist_mj(self.rect, self.cible.rect)>1550:
                self.cible=None


    def affichage(self, ecran, camx, camy):
        if self.direction== Direction.face:
            frames = assets.ASSETS['xeno_face']
        elif self.direction==Direction.droite:
            frames= assets.ASSETS['xeno_droite']
        elif self.direction ==Direction.gauche:
            frames = assets.ASSETS['xeno_gauche']
        else:
            frames= assets.ASSETS['xeno_back']
        self.time +=1
        if(self.time> self.vitesseanim):
            self.time=0
            self.animation=(self.animation+1)% len(frames)
        Xenojpeg= frames[self.animation %len(frames)]
        rect= Xenojpeg.get_rect(center =(self.rect.centerx + camx, self.rect.centery + camy))
        ecran.blit(Xenojpeg, rect)
        