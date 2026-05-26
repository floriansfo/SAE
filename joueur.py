import pygame
import math
import random
import assets
import option
import pygame as _pg
from prerequis import *
from prerequis import obstacle, angletrace
from arme import Arme

class Couteau:
    def __init__(self, joueur, ux, uy):
        self.id = 0
        self.joueur = joueur
        self.actif = True
        self.ux = ux
        self.uy = uy
        self.angle = -math.degrees(math.atan2(uy,ux))
        self.imgbase = assets.ASSETS.get('img_couteau')
        self.image = pygame.transform.rotate(self.imgbase, self.angle)
        self.rect = self.image.get_rect(center = joueur.rect.center)
        self.frame = 0
        self.duree = 15
        self.porte = 45
        self.touche = []
    
    def update(self):
        self.frame += 1
        if self.frame >= self.duree:
            self.actif = False
            return
        prog = math.sin((self.frame/self.duree)*math.pi)
        ext = prog*self.porte
        self.rect.centerx = self.joueur.rect.centerx + self.ux*ext
        self.rect.centery = self.joueur.rect.centery - self.uy*ext


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
        self.sonpas = assets.ASSETS.get('son_pas')
        self.soncut = assets.ASSETS.get('son_cut')
        #Oxygne
        self.oxygenemax = 21600
        self.oxygene = self.oxygenemax
        self.timeoxy = 0
        #Boutique
        self.pieces = 0
        self.malachite=0
        self.arsenal_achete = {0: True}
        self.achatjour = 0
        self.niveaudebloque = {1}
        self.possedelampe = True
        self.pile = 3600
        self.pilemax = 3600
        #Cristal
        self.cristal = False
        #Inventaire
        self.inventaire = [{"type": None, "quantite": 0} for _ in range(9)]
        self.inventaire[0] = {"type": "couteau", "quantite": 1}
        self.inventaire[1] = {"type": "lampe", "quantite": 1}        
        #Multi
        self.objjete = []
        self.objsol = []
        self.dsvaisseau = False
    
    def changerarme(self, num):
        if self.arsenal_achete.get(num, False):
            self.arsenal = num
    
    def updatetir(self, carte, objets, monstres, t):
        objetcasse = [] #Liste obj casse pour le serveur
        #Coultdown arme
        if self.vitessetir > 0:
            self.vitessetir -= 60*t
        #Mise a jour position des tirs
        tiractuelle = []
        for balle in self.tir:
            couteau = getattr(balle, "id", 1) == 0
            if couteau:
                balle.update()
                if not balle.actif:
                    continue
            else:
                balle.deplacer(t, self)
            touche_monstre= False
            for m in monstres:
                if not m.mort and balle.rect.colliderect(m.rect):
                        if couteau:
                            if m not in balle.touche:
                                m.take_damage(self.couteaudegat)
                                balle.touche.append(m)
                        else:
                            m.take_damage(10)
                            touche_monstre= True
                            break
            touche_objet = False
            for obj in objets:
                if balle.rect.colliderect(obj.rect) and obj.type in ["caisse", "meuble"]:
                    if couteau and obj in balle.touche:
                        continue
                    touche_objet = True
                    if couteau:
                        balle.touche.append(obj)
                    if not hasattr(obj, 'hp'):
                        obj.hp = 3
                    obj.hp -= 1
                    if obj.hp <= 0:
                        obj.type = "munition"
                        obj.texture = assets.ASSETS.get('img_munition', obj.texture)
                        obj.hitbox = obj.rect
                        objetcasse.append(obj)
                    if not couteau:
                        break
            if couteau:
                tiractuelle.append(balle)
            else:
                touche_mur = balle.collisionoupas(carte, objets)
                if not touche_monstre and not touche_objet and not touche_mur:
                    tiractuelle.append(balle)
        self.tir = tiractuelle
        return objetcasse

    def tirer(self):
        #Calcul de l'Appariton de la balle
        pangle = math.radians(self.angleactuel)
        debutx = self.rect.centerx + math.cos(pangle)*25
        debuty = self.rect.centery - math.sin(pangle)*25
        #On peut tirer que si on a des balle et que le couldown est fini
        if self.vitessetir <= 0:
            if self.arsenal == 0:
                if hasattr(self, "soncut") and self.soncut:
                    self.soncut.play()
                ux = math.cos(pangle)
                uy = math.sin(pangle)
                self.tir.append(Couteau(self, ux,uy))
                self.vitessetir = 25
            elif self.munition > 0:
                if self.arsenal == 1:
                    #Pistolet Classique
                    self.sonpistolet.play()
                    p = Arme(debutx, debuty, self.angleactuel, id=1)
                    self.tir.append(p)
                    self.vitessetir = 15
                    self.munition -= 1
                    self.retirer("munition", 1)
                elif self.arsenal == 2:
                    #Fusil a pompe: 2 balle
                    if self.munition>=2:
                        self.sonpompe.play()
                        #Tire 5 balle avec angles
                        for pompe in [-16, -8, 0, 8, 16]:
                            p = Arme(debutx, debuty, self.angleactuel+pompe, id=2)
                            self.tir.append(p)
                        self.vitessetir = 40
                        self.munition = self.munition - 2
                        self.retirer("munition", 2)
                elif self.arsenal == 3:
                    self.sonassaut.play()
                    #Fusil d'assaut: rapide avec recul entre -5 et 5 deg
                    recul = random.uniform(-5, 5)
                    p = Arme(debutx, debuty, self.angleactuel+recul, id=3)
                    self.tir.append(p)
                    self.vitessetir = 5
                    self.munition = self.munition - 1
                    self.retirer("munition", 1)

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
                mtn = pygame.time.get_ticks()
                if mtn-getattr(self, "dp",0)>350:
                    if hasattr(self, 'sonpas') and self.sonpas:
                        self.sonpas.play()
                    self.dp = mtn
        else:
            self.animation = 0
            self.time = 0
        #Tourner joueur vers souris
        fenetre = _pg.display.get_surface()
        sl, sh = fenetre.get_size()
        if not hasattr(self, 'sourisx'):
            self.sourisx = sl//2
            self.sourisy = sh//2
            pygame.mouse.get_rel()
        enjeu = not pygame.mouse.get_visible()            
        dx, dy = pygame.mouse.get_rel()
        if enjeu:
            pygame.mouse.set_pos((sl//2, sh//2))
            self.sourisx += dx*option.sensijoueur
            self.sourisy += dy*option.sensijoueur
        else:
            mx,my = pygame.mouse.get_pos()
            self.sourisx = mx
            self.sourisy = my
        self.sourisx = max(0, min(self.sourisx, sl))
        self.sourisy = max(0, min(self.sourisy, sh))
        tx = self.sourisx -sl//2
        ty = self.sourisy -sh//2
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
                self.possedelampe = False
                if hasattr(self, "retirer"):
                    self.retirer("lampe", 1)
    
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
    
    def quantite(self, type, quantite):
        for case in self.inventaire:
            if case["type"] == type:
                dispo = 64-case["quantite"]
                if dispo>0:
                    if quantite <= dispo:
                        case["quantite"] += quantite
                        return 0
                    else:
                        case["quantite"] = 64
                        quantite -= dispo
        if quantite > 0:
            for case in self.inventaire:
                if case["type"] is None:
                    case["type"] = type
                    if quantite <= 64:
                        case["quantite"] = quantite
                        return 0
                    else:
                        case["quantite"] = 64
                        quantite -= 64
        return quantite

    def retirer(self, type, quantite):
        for case in reversed(self.inventaire):
            if case["type"]==type:
                if case["quantite"] >= quantite:
                    case["quantite"] -= quantite
                    quantite = 0
                else:
                    quantite -= case["quantite"]
                    case["quantite"] = 0
                if case["quantite"] == 0:
                    case["type"] = None
                if quantite == 0:
                    return True
        return quantite == 0
    
    def jetobj(self, i, niveau_actuel):
        case = self.inventaire[i]
        if case["type"] is None or case["quantite"] == 0:
            return None
        if i == 0 and case["type"] == "couteau":
            return None
        objjetee = {"type": case["type"], "quantite": case["quantite"], "x": self.rect.centerx, "y": self.rect.centery, "etage": niveau_actuel}
        case["type"]=None
        case["quantite"]=0
        self.objjete.append(objjetee)
        return objjetee