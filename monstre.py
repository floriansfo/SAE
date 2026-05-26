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
        self.rect = pygame.Rect(x, y, 120, 125)
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
        #debloquer les loulous
        self.bloque =False
        #drop de minerai
        self.drop_malachite=[1,2,3]

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
        self.bloque =False
        #On regarde au tour les meubles present
        zone = self.rect.inflate(ZOOM*4, ZOOM*4)
        meubles = [obj.hitbox for obj in objets if obj.type == "meuble" and zone.colliderect(obj.rect)]
        #Collision X
        self.rect.x += kx
        ox = obstacle(self.rect,carte) + meubles
        x = self.rect.collidelistall(ox)
        for i in x:
            self.bloque=True
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
            self.bloque =True
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
        if self.hp_cur<= 0 and not self.mort: #Si pv sont a 0
            self.hp_cur= 0
            self.mort= True #Monstre meurt
            self.loot = random.randint(50, 100) #loot aléatoire entre 50 et 100 pièces
            self.loot_malachite= random.choice(self.drop_malachite)
        else:
            self.loot = 0
    
class Titan(Monstre):
    def __init__(self,x,y):
        super().__init__(x,y, speed=2, hp=999999)
        self.rect = pygame.Rect(x,y,80,80) #Hitbox
        self.hitbox = self.rect.inflate(-20,-20)
        self.hp = 99999
        self.degats = 35
        self.mort = False
        self.traque = True
        self.loot = 0
        self.lampejoueur = False
        self.recule = 0

    def deplacement(self, t, joueurx, joueury):
        #Recul balle
        if self.recule > 0:
            self.recule -= t
            return 0, 0 #Bouge plus
        #IA du titan qui se dirige vers le joueur
        px = joueurx - self.rect.centerx
        py = joueury - self.rect.centery
        dist = math.hypot(px, py) #Theoreme pytha pour la distance
        vitesse = 0
        if (dist < 450 and self.lampejoueur) or dist < 120:
            vitesse = 220 #T'attaque vite
        else:
            vitesse = 45 #Cherche pas
        kx, ky = 0,0
        if dist != 0:
            kx = (px/dist) * vitesse * t
            ky = (py/dist) * vitesse * t
        return kx, ky
    
    def collision(self, kx, ky, carte, objets):
        #Si le monstre touche un mur il le traverse
        self.rect.x += kx
        self.rect.y += ky



#spawn des monstres par étage
def spawn_metage(niveau, salles):
    from mimique import Mimique
    from slime import Slime
    from nyctobat import Nyctobat
    from errant import Errant
    from xeno import Xeno
    monstres=[]
    #choix des nv de spawn des monstres
    if niveau==1:
        nb_slime=6
        nb_mimique=0
        nb_nyctobat=0
        nb_errant=0
        nb_xeno=0
        nb_titan=0
    elif niveau==2:
        nb_slime=8
        nb_mimique=1
        nb_nyctobat=3
        nb_errant=1
        nb_xeno=0
        nb_titan=0
    elif niveau==3:
        nb_slime=10
        nb_mimique=2
        nb_nyctobat=3
        nb_errant=0
        nb_xeno=0
        nb_titan=0
    elif niveau==4:
        nb_slime=8
        nb_mimique=2
        nb_nyctobat=4
        nb_errant=1
        nb_xeno=0
        nb_titan=0
    elif niveau==5:
        nb_slime=11
        nb_mimique=3
        nb_nyctobat=2
        nb_errant=2
        nb_xeno=1
        nb_titan=0
    elif niveau==6:
        nb_slime=12
        nb_mimique=2
        nb_nyctobat=3
        nb_errant=1
        nb_xeno=2
        nb_titan=1
    else:
        nb_slime=0
        nb_mimique=0
        nb_nyctobat=0
        nb_errant=0
        nb_xeno=0
        nb_titan=0
    for i in range(nb_mimique):
        salle=  random.choice(salles)
        mx= salle.centerx * ZOOM
        my = salle.centery *ZOOM
        monstres.append(Mimique(mx, my))
    for i in range(nb_slime):
        salle=  random.choice(salles)
        mx= salle.centerx * ZOOM
        my = salle.centery *ZOOM
        monstres.append(Slime(mx, my))
    for i in range(nb_nyctobat):
        salle=  random.choice(salles)
        mx= salle.centerx * ZOOM
        my = salle.centery *ZOOM
        monstres.append(Nyctobat(mx, my))
    for i in range(nb_errant):
        salle=  random.choice(salles)
        mx= salle.centerx * ZOOM
        my = salle.centery *ZOOM
        monstres.append(Errant(mx, my))
    for i in range(nb_xeno):
        salle=  random.choice(salles)
        mx= salle.centerx * ZOOM
        my = salle.centery *ZOOM
        monstres.append(Xeno(mx, my))
    for i in range(nb_titan):
        salle=  random.choice(salles)
        mx= salle.centerx * ZOOM
        my = salle.centery *ZOOM
        monstres.append(Titan(mx, my))
    return monstres


class Direction:
    face= 'face'
    droite= 'droite'
    gauche= 'gauche'
    back ='back'
    def mouvement(dx, dy):
        if(abs(dx)> abs(dy)):
            if dx>0:
                return Direction.droite
            else:
                return Direction.gauche
        elif dy>0:
            return Direction.face
        else:
            return Direction.back
    