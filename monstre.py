import pygame
import random
import math
import assets
from prerequis import obstacle, texture, ZOOM



#lst des mouvement pour que le random choisissent
move = [-1, 0, 1]

class Monstre:
    def __init__(self,x, y, speed, hp):
        #Hitbox et pos
        self.rect = pygame.Rect(x, y, 200, 200)
        self.rect.center = (x, y)
        #vitesse
        self.speed = speed
        #La vie
        self.hp_cur= hp
        self.hp_max=hp
        self.mort=False
        #mouvement aléatoire
        self.pos_x = random.choice(move)
        self.pos_y = random.choice(move)
        #Texture
        self.texture= assets.ASSETS['img_larry']

    #Calcul du deplacement en fct de la position du joueur
    def deplacement(self, t, joueur_x=None, joueur_y = None):
        kx= self.pos_x * self.speed*60*t
        ky = self.pos_y * self.speed*60*t
        if joueur_x is not None and joueur_y is not None :
            dx = joueur_x -self.rect.centerx
            dy = joueur_y - self.rect.centery
            #Distance avec le joueur calcul
            distance =math.hypot(dx,dy)
            #Lorsque le joueur est proche
            if distance <500 and distance >0:
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

    def collision(self, kx, ky, carte, objets):
        #On regarde au tour les meubles present
        zone = self.rect.inflate(ZOOM*4, ZOOM*4)
        meubles = [obj.hitbox for obj in objets if obj.type == "meuble" and zone.colliderect(obj.rect)]
        #Collision X
        self.rect.x += kx
        ox = obstacle(self.rect,carte) + meubles
        x = self.rect.collidelistall(ox)
        for i in x:
            if kx >0: #Vers la droite
                self.rect.right = ox[i].left
                self.pos_x= -1 #On le pousse pour eviter collision
            if kx <0:
                self.rect.left = ox[i].right
                self.pos_x=1

        #Collision Y
        self.rect.y += ky
        oy = obstacle(self.rect,carte) + meubles
        y = self.rect.collidelistall(oy)
        for i in y:
            if ky >0:
                self.rect.bottom = oy[i].top
                self.pos_y = -1
            if ky <0:
                self.rect.top = oy[i].bottom
                self.pos_y = 1
    
#affichage de l'image
    def affichage(self, ecran, camera_x, camera_y):
        fenetre_x=self.rect.x + camera_x
        fenetre_y = self.rect.y + camera_y
        ecran.blit(self.texture, (fenetre_x, fenetre_y))
    
    def take_damage(self, degats):
        self.hp_cur -= degats
        if self.hp_cur<= 0: #Si pv sont a 0
            self.hp_cur= 0
            self.mort= True #Monstre meurt
            self.loot = random.randint(50, 100) #loot aléatoire entre 50 et 100 pièces
        else:
            self.loot = 0
    
class Titan(Monstre):
    texture_cache = None
    def __init__(self,x,y, speed =4.0, hp = 1500):
        super().__init__(x,y,speed,hp)
        self.rect = pygame.Rect(x,y,100,100) #Hitbox
        self.rect.center = (x,y)
        self.degats = 25
        self.traque = True
        if Titan.texture_cache is None:
            imgbase = assets.ASSETS['img_larry']
            Titan.texture_cache = pygame.transform.scale(imgbase, (200,200))
            Titan.texture_cache.fill((200,0,0,100), special_flags=pygame.BLEND_RGBA_MULT)
        self.texture = Titan.texture_cache

    def deplacement(self, t, joueurx = None, joueury = None):
        #IA du titan qui se dirige vers le joueur
        if joueurx is not None and joueury is not None:
            px = joueurx - self.rect.centerx
            py = joueury - self.rect.centery
            dist = math.sqrt(px*px + py*py) #Theoreme pytha pour la distance
            if dist > 0:
                kx = (px/dist)*self.speed*60*t
                ky = (py/dist)*self.speed*60*t
                return (kx, ky)
        return super().deplacement(t,joueurx,joueury)
    
    def collision(self, kx, ky, carte, objets):
        #Si le monstre touche un mur il le traverse
        self.rect.x += kx
        self.rect.y += ky

