import pygame
import random
import math
import assets
from monstre import Monstre, move
from prerequis import dist_mj



class Slime (Monstre) :
    nb_etage=7
    def __init__(self, x, y,):
        super().__init__(x, y, 2, 100)
        self.degats=8
        #Anim
        self.animation=0
        self.time=0
        self.vitesseanim=5
        self.angle=0
        self.angle_cible=0
        #couleur
        self.couleur= random.choice(assets.ASSETS['couleurs_slime'])
        self.frame=[]
        for frame in assets.ASSETS['slime_move']:
            tmp =frame.copy()
            tmp.fill(self.couleur, special_flags=pygame.BLEND_RGB_ADD)
            self.frame.append(tmp)
    def deplacement(self, t, joueur_x=None, joueur_y=None):
        if(random.random()<0.02):
            self.pos_x= random.choice(move)
            self.pos_y= random.choice(move)
            if self.pos_x !=0 or self.pos_y!=0:
                self.angle_cible = math.degrees(math.atan2(-self.pos_y, self.pos_x))
        rota_valeur=3
        if abs(self.angle- self.angle_cible)<=rota_valeur:
            self.angle = self.angle_cible
        if (self.angle<self.angle_cible):
            self.angle+=rota_valeur
        elif (self.angle> self.angle_cible):
            self.angle -=rota_valeur
        kx= self.pos_x*self.speed*60*t
        ky= self.pos_y * self.speed*60*t  
        return (kx, ky)
    


    def affichage(self, ecran, camx, camy):
        x= self.rect.x +camx
        y= self.rect.y +camy
        if self.pos_x !=0 or self.pos_y !=0:
            self.time+=1
            if self.time > self.vitesseanim:
                self.time = 0
                self.animation = (self.animation+1)% len(self.frame)
        else:
            self.animation=0
    
        #affichage tourner
        jpegslime = pygame.transform.rotate(self.frame[self.animation], self.angle)
        rectaffiche = jpegslime.get_rect(center = (self.rect.centerx + camx, self.rect.centery + camy))
        ecran.blit(jpegslime, rectaffiche)
        
        

