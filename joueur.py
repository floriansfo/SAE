import pygame
import math
import random
import assets
import pygame as _pg
from prerequis import *
from prerequis import obstacle, angletrace
from arme import Arme

class Joueur:
    def __init__(self, x, y):
        #Hitbox et pos
        self.rect = pygame.Rect(x, y, 40, 40)
        self.rect.center = (x, y)
        #Rotation
        self.angle = 0
        self.angleactuel = 0
        self.dernierkx = 1
        self.dernierky = 0
        #Animation
        self.animation = 0
        self.time = 0
        self.vitesseanim = 5
        self.lumiereallumee = False
        #Deplacement
        self.marche = 7
        self.course = 11
        self.maxcourse = 100
        self.endurance = self.maxcourse
        #Armes
        self.tir = []
        self.vitessetir = 0
        self.delaytir = 12
        self.munition = 0
        self.arsenal = 0
        self.couteautemps = 0
        self.couteaudegat = 25
        self.couteauporte = 80
        #vie
        self.hpmax=100
        self.hp= self.hpmax
        self.god=0
        #Sons
        self.sonpistolet = assets.ASSETS['son_pistolet']
        self.sonpompe = assets.ASSETS['son_pompe']
        self.sonassaut = assets.ASSETS['son_assaut']
        #Oxygne
        self.oxygenemax = 21600
        self.oxygene = self.oxygenemax
        self.timeoxy = 0
        #Boutique
        self.pieces = 0
        self.arsenal_achete = {0: True}
        self.achatjour = 0
        self.niveaudebloque = {1}
        self.possedelampe = True
        self.pile = 3600
        self.pilemax = 3600
        #Cristal
        self.cristal = False

    def changerarme(self, num):
        if self.arsenal_achete.get(num, False):
            self.arsenal = num
    
    def updatetir(self, carte, objets, monstres, t):
        objetcasse = [] #Liste obj casse pour le serveur
        #Coultdown arme
        if self.vitessetir > 0:
            self.vitessetir -= 60*t
        if self.couteautemps > 0:
            self.couteautemps -= 60*t
        #Mise a jour position des tirs
        tiractuelle = []
        for balle in self.tir:
            balle.deplacer(t)
            touche_monstre= False
            for m in monstres:
                if not m.mort and balle.rect.colliderect(m.rect):
                        m.take_damage(10)
                        touche_monstre= True
            if not touche_monstre :
                zone = balle.rect.inflate(ZOOM*4, ZOOM*4)
                objproche = [obj for obj in objets if zone.colliderect(obj.rect)]
                touche = balle.collisionoupas(carte, objproche)
                limx = HAUTEURMAP*ZOOM
                limy = HAUTEURMAP*ZOOM
                if not touche and (-1000<balle.rect.x<limx+1000) and (-1000<balle.rect.y<limy+1000):
                    tiractuelle.append(balle)
                elif touche and touche != "mur": 
                    #Touche objet destructible
                    if not hasattr(touche, 'hp'):
                        touche.hp = 3
                    touche.hp = touche.hp -1
                    if touche.hp <= 0:
                        #La caisse se casse et se transforme en muni
                        touche.type = "munition"
                        touche.texture = assets.ASSETS['img_munition']
                        touche.hitbox = touche.rect
                        objetcasse.append(touche)
        self.tir = tiractuelle
        return objetcasse

    def tirer(self):
        #On peut tirer que si on a des balle et que le couldown est fini
        if self.munition>0 and self.vitessetir <= 0:
            #Calcul de l'Appariton de la balle
            pangle = math.radians(self.angleactuel)
            debutx = self.rect.centerx + math.cos(pangle)*20
            debuty = self.rect.centery - math.sin(pangle)*20
            if self.arsenal == 1:
                #Pistolet Classique
                self.sonpistolet.play()
                p = Arme(debutx, debuty, self.angleactuel)
                self.tir.append(p)
                self.vitessetir = 15
                self.munition -= 1
            elif self.arsenal == 2:
                #Fusil a pompe: 2 balle
                if self.munition>=2:
                    self.sonpompe.play()
                    #Tire 5 balle avec angles
                    for pompe in [-16, -8, 0, 8, 16]:
                        p = Arme(debutx, debuty, self.angleactuel+pompe)
                        self.tir.append(p)
                    self.vitessetir = 40
                    self.munition = self.munition - 2
            elif self.arsenal == 3:
                self.sonassaut.play()
                #Fusil d'assaut: rapide avec recul entre -5 et 5 deg
                recul = random.uniform(-5, 5)
                p = Arme(debutx, debuty, self.angleactuel+recul)
                self.tir.append(p)
                self.vitessetir = 5
                self.munition = self.munition - 1

    def attaquecouteau(self, monstres):
        if self.couteautemps>0:
            return []
        touches = []
        for m in monstres:
            if not m.mort:
                dist = math.hypot(m.rect.centerx-self.rect.centerx, m.rect.centery-self.rect.centery)
                if dist < self.couteauporte:
                    m.take_damage(self.couteaudegat)
                    touches.append(m)
        self.sonassaut.play()
        if touches:
            self.couteautemps = 30
        else:
            self.couteautemps = 20
        return touches

    def deplacer(self, keys, nb_frame, t):
        vitessecourse = self.course*60*t
        vitessemarche = self.marche*60*t
        vitesse = vitessemarche
        mouvement = False
        #Verifie si se déplace
        if keys[pygame.K_LEFT] or keys[pygame.K_q] or keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_UP] or keys[pygame.K_z] or keys[pygame.K_DOWN] or keys[pygame.K_s]:    
            mouvement = True
        #Sprint avec shift
        if mouvement == True and keys[pygame.K_LSHIFT] and self.endurance > 0:
            vitesse = vitessecourse
            self.endurance -= 0.5
        else:
            if self.endurance < self.maxcourse:
                self.endurance += 0.1

        #Commande et calcul de deplacement
        kx, ky = 0,0
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            kx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            kx += 1
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            ky -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            ky += 1
        
        #Direction avant de bouger
        if kx !=0 and ky !=0:
            self.dernierkx, self.dernierky = kx,ky

        #Diagonale meme vitesse
        if kx !=0 and ky !=0:
            kx *=0.707
            ky *=0.707
        
        kx *= vitesse
        ky *= vitesse

        #Mise a jour angle
        if kx !=0 or ky != 0:
            self.dernierkx, self.dernierky=kx,ky
            self.time +=1
            if self.time > self.vitesseanim:
                self.time = 0
                self.animation = (self.animation+1)%nb_frame
        else:
            self.animation = 0
            self.time = 0
        #Tourner joueur vers souris
        sx, sy = pygame.mouse.get_pos()
        fenetre = _pg.display.get_surface()
        sl, sh = fenetre.get_size()
        tx = sx-sl//2
        ty = sy-sh//2
        self.angleactuel = math.degrees(math.atan2(-ty, tx))
        self.angle = self.angleactuel + 90
        return kx, ky
    
    def collision(self, kx, ky, carte, objets, moteurrect=None):
        #On lit les meubles au tour
        zone = self.rect.inflate(ZOOM*4, ZOOM*4)
        #Hitbox des meubles au tour pour opti
        meubles = [obj.hitbox for obj in objets if obj.type == "meuble" and zone.colliderect(obj.rect)]

        if moteurrect and zone.colliderect(moteurrect):
            meubles.append(moteurrect)

        #Collision X
        self.rect.x += kx
        ox = obstacle(self.rect,carte) + meubles
        x = self.rect.collidelistall(ox)
        for i in x:
            if kx >0:
                self.rect.right = ox[i].left
            if kx <0:
                self.rect.left = ox[i].right

        #Collision Y
        self.rect.y += ky
        oy = obstacle(self.rect,carte) + meubles
        y = self.rect.collidelistall(oy)
        for i in y:
            if ky >0:
                self.rect.bottom = oy[i].top
            if ky <0:
                self.rect.top = oy[i].bottom

    def toogle_lumiere(self):
        if not self.possedelampe:
            return  
        if self.pile <= 0:
            self.lumiereallumee = False
            return
        self.lumiereallumee = not self.lumiereallumee
    
    def updatelampe(self, mode_combat= False):
        if self.lumiereallumee and self.possedelampe and not mode_combat:
            self.pile -= 1
            if self.pile <= 0:
                self.pile = 0
                self.lumiereallumee = False
    
    def updateoxygene(self, niveau_actuel):
        if niveau_actuel != 0:
            if self.oxygene > 0:
                self.oxygene -= 1
            else:
                self.timeoxy += 1
                if self.timeoxy >= 60:  # Perte de vie toutes les secondes
                    self.timeoxy = 0
                    self.hp -= 5
        else:
            self.oxygene = self.oxygenemax