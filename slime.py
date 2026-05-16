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
        self.frames_mort=[]
        for frame in assets.ASSETS['slime_die']:
            tmp =frame.copy()
            tmp.fill(self.couleur, special_flags=pygame.BLEND_RGB_ADD)
            self.frames_mort.append(tmp)
        #la mort du slime au slime
        self.anim_mort=False
        self.frame_mort =0
        self.time_mort=0

    
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
    


    def take_damage(self, degats):
        super().take_damage(degats)
        if self.mort:
            self.mort= False
            self.anim_mort=True
            self.degats=0

    def affichage(self, ecran, camx, camy):
        x= self.rect.x +camx
        y= self.rect.y +camy
        if self.anim_mort:
            self.time_mort+=1
            if self.time_mort> self.vitesseanim:
                self.time_mort=0
                self.frame_mort+=1
                if self.frame_mort>=len(self.frames_mort):
                    self.mort=True
                    self.frame_mort=len(self.frames_mort)-1 
            jpegslime = pygame.transform.rotate(self.frames_mort[self.frame_mort], self.angle)
            rectaffiche = jpegslime.get_rect(center = (self.rect.centerx + camx, self.rect.centery + camy))
            ecran.blit(jpegslime, rectaffiche)
            return

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
        
        

