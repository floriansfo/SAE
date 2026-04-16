import pygame
import random
import math
import assets
from monstre import Monstre, move
from joueur import Joueur
from prerequis import obstacle, texture, ZOOM




class Mimique(Monstre):
    def __init__(self, x, y, speed, hp):
        super().__init__(x, y, 2.8, 3000)
        self.rage=False
        self.cible=None
        self.timer= 0.0
        self.revil=True
        self.timer_revil=0.0
        self.animation=0
        self.time= 0
        self.vitesseanim = 5

    def deplacement(self, t, joueur_x=None, joueur_y = None):
        kx= self.pos_x * self.speed*60*t
        ky = self.pos_y * self.speed*60*t
        if self.cible is not None:
            dx = self.cible.rect.centerx -self.rect.centerx
            dy = self.cible.rect.centery - self.rect.centery
            #Distance avec le joueur calcul
            distance =math.hypot(dx,dy)
            if not self.enrage and distance <250:
                return (0,0)
            #Lorsque le joueur est proche
            if distance >0:
                kx = (dx/distance) *self.speed*60*t
                ky = (dy/distance) *self.speed*60*t
                return (kx, ky)
        #sinon ça fait des choses aléatoires 
        if(random.random()<0.02):
            self.pos_x= random.choice(move)
            self.pos_y= random.choice(move)
        else:
            kx= self.pos_x*self.speed*60*t
            ky= self.pos_y * self.speed*60*t  
        return (kx, ky)
    
    def mrage(self):
        self.speed = 7
        self.enrage=True
        self.revil=True
        self.texture= assets.ASSETS['img_larry']

    def comportement(self,t, joueurs) :
        if self.enrage==True:
            return
        if not self.cible:
            for joueur in joueurs:
                dx = joueur.rect.centerx -self.rect.centerx
                dy = joueur.rect.centery - self.rect.centery
                if math.hypot(dx, dy)<600:
                    self.cible =joueur
                    self.timer =0.0
                    return
        
        dx = self.cible.rect.centerx -self.rect.centerx
        dy = self.cible.rect.centery - self.rect.centery
        dist=math.hypot(dx, dy)
        if dist>1550:
            self.cible=None
            self.timer=0.0
            return
        self.timer+=t
        if self.timer>=8.0:
            self.mrage()
    
    def take_damage(self, degats):
        super().take_damage(degats)
        self.loot=0
        if not self.enrage and not self.mort:
            self.mrage()

    def affichage(self, ecran, camx, camy):
        x= self.rect.x +camx
        y= self.rect.y +camy
        if not self.enrage:
            self.time+=1
            if self.time > self.vitesseanim:
                self.time = 0
                self.animation = (self.animation+1)% len(assets.ASSETS['animationjoueur'])
            ecran.blit(assets.ASSETS['animationjoueur'][self.animation],(x,y))
        else:
            ecran.blit(self.texture, (x,y))