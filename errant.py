import pygame
import random
import math
import assets
from monstre import Monstre, move, Direction
from prerequis import dist_mj
import lumiere



class Errant(Monstre):
    nb_etage=15
    def __init__(self, x, y,):
        super().__init__(x, y, 1, 100)
        self.degats= 25
        self.cible=None
        self.direction= Direction.face
        #animation
        self.animation=0
        self.time=0
        self.vitesseanim=5

    
    def deplacement(self, t, joueur_x=None, joueur_y = None):
        if self.cible is not None:
            self.speed=7
        else:
            self.speed=1
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
        #deterction de cible avec lampe
        if not self.cible:
            for joueur in joueurs:
                if joueur.lumiereallumee:
                    self.cible =joueur
        else:
            #puis part si trop loin
            if not self.cible.lumiereallumee:
                self.cible=None

    def take_damage(self, degats):
        super().take_damage(degats)
        if self.mort:
            self.loot= 200




    def affichage(self, ecran, camx, camy):
        if self.direction== Direction.face:
            frames = assets.ASSETS['errant_face']
        elif self.direction==Direction.droite:
            frames= assets.ASSETS['errant_droite']
        elif self.direction ==Direction.gauche:
            frames = assets.ASSETS['errant_gauche']
        else:
            frames= assets.ASSETS['errant_back']
        self.time +=1
        if(self.time> self.vitesseanim):
            self.time=0
            self.animation=(self.animation+1)% len(frames)
        errantjpeg= frames[self.animation]
        rect= errantjpeg.get_rect(center = (self.rect.centerx + camx, self.rect.centery + camy))
        ecran.blit(errantjpeg, rect)
        