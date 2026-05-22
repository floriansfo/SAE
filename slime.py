import pygame
import random
import assets
from monstre import Monstre, move, Direction
from prerequis import dist_mj



class Slime (Monstre) :
    def __init__(self, x, y,):
        super().__init__(x, y, 2, 100)
        self.degats=8
        self.direction= Direction.face
        #Anim
        self.animation=0
        self.time=0
        self.vitesseanim=5
        #couleur aléatoir defini dans assets
        self.couleur= random.choice(assets.ASSETS['couleurs_slime'])
        #teinte du slime
        self.face= self.slime_couleur(assets.ASSETS['slime_face'])
        self.back= self.slime_couleur(assets.ASSETS['slime_back'])
        self.gauche= self.slime_couleur(assets.ASSETS['slime_gauche'])
        self.droite= self.slime_couleur(assets.ASSETS['slime_droite'])
        #teinte mort
        self.face_mort= self.slime_couleur(assets.ASSETS['slime_mort_face'])
        self.back_mort= self.slime_couleur(assets.ASSETS['slime_mort_back'])
        self.gauche_mort= self.slime_couleur(assets.ASSETS['slime_mort_gauche'])
        self.droite_mort= self.slime_couleur(assets.ASSETS['slime_mort_droite'])
        #la mort du slime
        self.anim_mort=False
        self.frame_mort=0
        self.time_mort=0
        self.drop_malachite=[1]

       
    
    def slime_couleur(self, frames):
        lst=[]
        for frame in frames:
            tmp =frame.copy()
            tmp.fill(self.couleur, special_flags=pygame.BLEND_RGB_ADD)
            lst.append(tmp)
        return lst
    
    def deplacement(self, t, joueur_x=None, joueur_y=None):
        if self.anim_mort:
            return (0,0)
        if self.pos_x !=0 or self.pos_y!=0:
            self.direction= Direction.mouvement(self.pos_x, self.pos_y)        
        if(random.random()<0.01):
            self.pos_x= random.choice(move)
            self.pos_y= random.choice(move)
            if self.pos_x !=0 or self.pos_y!=0:
                self.direction= Direction.mouvement(self.pos_x, self.pos_y)  
        kx= self.pos_x*self.speed*60*t
        ky= self.pos_y * self.speed*60*t  
        return (kx, ky)
    


    def take_damage(self, degats):
        super().take_damage(degats)
        if self.mort:
            #avant de le tuer on fait l'anim
            self.mort= False
            self.anim_mort=True
            self.degats=0

    def affichage(self, ecran, camx, camy):
        if self.anim_mort:
            self.affichage_mort(ecran, camx, camy)
        else:
            self.affichage_marche(ecran, camx, camy)
    
    def affichage_marche(self, ecran, camx, camy):
        if self.direction== Direction.face:
            frames = self.face
        elif self.direction==Direction.droite:
            frames= self.droite
        elif self.direction ==Direction.gauche:
            frames = self.gauche
        else:
            frames= self.back
        if self.pos_x !=0 or self.pos_y !=0:
            self.time+=1
            if(self.time> self.vitesseanim):
                self.time=0
                self.animation=(self.animation+1)% len(frames)
        else:
            self.animation=0
        slimejpeg= frames[self.animation %len(frames)]
        rect= slimejpeg.get_rect(center = (self.rect.centerx + camx, self.rect.centery + camy))
        ecran.blit(slimejpeg, rect)
        
    def affichage_mort(self, ecran, camx, camy):
        if self.direction== Direction.face:
            frames_mort = self.face_mort
        elif self.direction==Direction.droite:
            frames_mort = self.droite_mort
        elif self.direction ==Direction.gauche:
            frames_mort = self.gauche_mort
        else:
            frames_mort= self.back_mort
        self.time_mort +=1
        if(self.time_mort> self.vitesseanim):
            self.time_mort =0
            self.frame_mort+=1
            if self.frame_mort>=len(frames_mort):
                self.mort=True
                self.frame_mort= len(frames_mort)-1
        slimejpeg= frames_mort[self.frame_mort]
        rect= slimejpeg.get_rect(center = (self.rect.centerx + camx, self.rect.centery + camy))
        ecran.blit(slimejpeg, rect)
    
     
        

