import pygame
import random
import assets

VERTFOND = (10,25,15,210)
VERTBORD = (45,90,55)
VERTPHOSPHORE = (100,255,150)
VERTECLAT = (180,255,200)
BLANC = (240,255,240)
ROUGE = (255,60,60)
ORANGE =(255,170,50)
BLEU = (100,180,255)

class Overlay:
    def __init__(self, largeur, hauteur):
        self.L = largeur
        self.H = hauteur
        #Cache pour opti
        self.CACHE = {}
        self.imgmodebase = assets.ASSETS.get('mode_combat')
        self.imginventairebase = assets.ASSETS.get('mode_inventaire')
        self.coeurbase = assets.ASSETS.get('coeur_hp')
        self.update_dimensions(self.L, self.H)

    def update_dimensions(self, L, H):
        self.L = L
        self.H = H
        self.surfalpha = pygame.Surface((self.L, self.H), pygame.SRCALPHA)
        self.CACHE.clear()
        #Echelle image
        self.echelle = self.H/1080.0
        #Redimensionne les polices
        self.police = pygame.font.Font("ressource/police.ttf", max(12, int(24*self.echelle)))
        self.arme_police = pygame.font.Font("ressource/police.ttf", max(16, int(40*self.echelle)))
        self.policemode = pygame.font.Font("ressource/police.ttf", max(24, int(48*self.echelle)))
        self.policeoxy = pygame.font.Font("ressource/titre.ttf", max(12, int(24*self.echelle)))
        #Redimensionne les images
        self.imgmode = pygame.transform.scale(self.imgmodebase, (int(self.imgmodebase.get_width()*self.echelle), int(self.imgmodebase.get_height()*self.echelle)))
        self.imginventaire = pygame.transform.scale(self.imginventairebase, (int(self.imginventairebase.get_width()*self.echelle), int(self.imginventairebase.get_height()*self.echelle)))
        self.coeur = pygame.transform.scale(self.coeurbase, (int(self.coeurbase.get_width()*self.echelle), int(self.coeurbase.get_height()*self.echelle)))
        self.arme_imgmode= pygame.transform.scale(self.imgmode, (int(260*self.echelle), int(60*self.echelle)))

    def textee(self, police, texte, couleur):
        cle = (texte, couleur)
        if cle not in self.CACHE:
            self.CACHE[cle] = police.render(texte, True, couleur)
        return self.CACHE[cle]

    def panneau(self, fenetre, x, y, w, h):
        self.surfalpha.fill((0,0,0,0), (x,y,w,h))
        #Fond
        pygame.draw.rect(self.surfalpha, VERTFOND, (x,y,w,h), border_radius=4)
        fenetre.blit(self.surfalpha, (x,y), (x,y,w,h))
        #Bordure
        pygame.draw.rect(fenetre, VERTBORD, (x,y,w,h), max(1, int(3*self.echelle)))
        #Coin eclairé
        pygame.draw.line(fenetre, VERTPHOSPHORE, (x,y+int(self.echelle*6)), (x, y+int(self.echelle*16)), max(1, int(3*self.echelle)))
        pygame.draw.line(fenetre, VERTPHOSPHORE, (x+int(self.echelle*6),y), (x+int(self.echelle*16), y), max(1, int(3*self.echelle)))

    def onventaire(self, fenetre, inventaire):
        if inventaire:
            dessus = self.imginventaire.get_rect(center = (self.L//2, self.H//2))
            fenetre.blit(self.imginventaire, dessus)

    def mode_texte(self, fenetre, m_combat, enpause, inventaire):
        marge = int(10*self.echelle)
        fenetre.blit(self.imgmode, (marge, marge))
        if enpause:
            texte = "PAUSE"
        elif inventaire:
            texte = "INVENTAIRE"
        elif m_combat == True:
            texte = "COMBAT"
        else:
            texte = "EXPLORATION"
        surface = self.textee(self.policemode, texte, BLANC)
        surfacerect = surface.get_rect()
        surfacerect.center = (marge+self.imgmode.get_width()//2, marge+self.imgmode.get_height()//2)
        fenetre.blit(surface, surfacerect)

    def pieces(self, fenetre, joueur):
        texte = self.textee(self.police, f"PIECES: {joueur.pieces}", ORANGE)
        w,h = texte.get_width()+int(30*self.echelle), int(40*self.echelle)
        x,y = self.L-w-int(10*self.echelle), int(65*self.echelle)
        self.panneau(fenetre, x, y, w, h)
        fenetre.blit(texte, texte.get_rect(center=(x+w//2, y+h//2)))

    def horloge(self, fenetre, jour, heure):
        DUREE = 28800
        heure = min(heure, DUREE)
        heurejeu = 6+(heure/DUREE)*14
        heures, minutes = int(heurejeu), int((heurejeu-int(heurejeu))*60)
        restant = DUREE-heure
        if restant>7200:
            couleur = VERTPHOSPHORE
        elif restant>2880:
            couleur = ORANGE
        else:
            couleur = ROUGE
        texte = self.textee(self.police, f"JOUR {jour} | {heures:02d}:{minutes:02d}", couleur)
        w,h = texte.get_width()+int(30*self.echelle), int(45*self.echelle)
        x,y = self.L-w-int(10*self.echelle), int(10*self.echelle)
        self.panneau(fenetre, x, y, w, h)
        fenetre.blit(texte, texte.get_rect(center=(x+w//2, y+h//2)))
        if heurejeu >= 18 and pygame.time.get_ticks()%1000<500:
            alerte = self.textee(self.police, "ALERTE: RENTRER AU VAISSEAU", ROUGE)
            fenetre.blit(alerte, alerte.get_rect(center=(self.L//2, int(80*self.echelle))))

   # def arme_overlay(self, fenetre, joueur, image, present):
    #    posx = int((415+(present//4))*self.echelle)
     #   posy = self.H-int(62*self.echelle)
      #  imgarme = image.get(joueur.arsenal)
       # imgarme = pygame.transform.scale(imgarme, (int(160*self.echelle), int(40*self.echelle)))
        #fenetre.blit(imgarme, (posx, posy))
    
    def arme_overlay(self, fenetre, joueur, image, present):
        if joueur.arsenal == -1:
            return
        if joueur.arsenal==3:
            arme_nom="FUSIL"
        elif joueur.arsenal==2:
            arme_nom="POMPE"
        elif joueur.arsenal==1:
            arme_nom="PISTOLET"
        else:
            arme_nom="COUTEAU"
        posx = int((320+(present//4))*self.echelle)
        posy = self.H-int(50*self.echelle)-self.imgmode.get_height()-int(5*self.echelle)
        fenetre.blit(self.arme_imgmode, (posx, posy))
        surface = self.textee(self.arme_police, arme_nom, BLANC)
        surfacerect = surface.get_rect()
        surfacerect.center = (posx+self.arme_imgmode.get_width()//2, posy+self.arme_imgmode.get_height()//2)
        fenetre.blit(surface, surfacerect)

    def munition(self, fenetre, joueur, img):
        self.panneau(fenetre, int(320*self.echelle), self.H-int(71*self.echelle), int(260*self.echelle), int(60*self.echelle))
        couleur = VERTPHOSPHORE if joueur.munition > 0 else ROUGE
        texte = self.textee(self.police, f"x{joueur.munition}", couleur)
        posx = int(340*self.echelle)
        posy = int(self.H-(56*self.echelle))
        imgvert = img.copy()
        imgvert.fill(VERTPHOSPHORE, special_flags=pygame.BLEND_RGBA_MULT)
        imgvert = pygame.transform.scale(imgvert, (int(50*self.echelle), int(50*self.echelle)))
        fenetre.blit(imgvert, (posx-int(8*self.echelle), posy-int(10*self.echelle)))
        fenetre.blit(texte, (posx+int(40*self.echelle), posy+int(3*self.echelle)))

    def endurance(self, fenetre, joueur, course):
        largeur, hauteur = int(240*self.echelle), int(10*self.echelle)
        x,y = self.L//2-largeur//2, self.H-int(30*self.echelle)
        fin = joueur.endurance/joueur.maxcourse
        couleur = VERTECLAT if fin >0.25 else ROUGE
        pygame.draw.rect(fenetre, (20,30,20), (x, y, largeur, hauteur), border_radius=3)
        if fin >0:
            pygame.draw.rect(fenetre, couleur, (x, y, int(fin*largeur), hauteur), border_radius=3)
        pygame.draw.rect(fenetre, VERTBORD, (x, y, largeur, hauteur), 1, border_radius=3)
        #Etincelle quand course
        if course and fin >0 :
            for _ in range(5):
                px, py = random.randint(-5,5), random.randint(-2, hauteur+2)
                pygame.draw.circle(fenetre, VERTECLAT, (int(x+(fin*largeur)+px), int(y+py)),1)

    def lampe(self, fenetre, joueur,img_lampe):
        self.panneau(fenetre, int(15*self.echelle), self.H-int(131*self.echelle), int(290*self.echelle), int(120*self.echelle))
        x,y = int(30*self.echelle), self.H-int(115*self.echelle)
        if not joueur.possedelampe:
            texte = self.textee(self.police, "LUM: --", ROUGE)
            fenetre.blit(texte, (x,y))
            return
        p = int((joueur.pile/joueur.pilemax)*100)
        if p >50:
            couleur = VERTPHOSPHORE
        elif p > 20:
            couleur = ORANGE
        else:
            couleur = ROUGE
        imglampe = img_lampe.copy()
        imglampe.fill(couleur, special_flags=pygame.BLEND_RGB_ADD)
        imglampe = pygame.transform.scale(imglampe, (int(40*self.echelle), int(40*self.echelle)))
        fenetre.blit(imglampe, (x,y-int(10*self.echelle)))
        etat = "ON" if joueur.lumiereallumee else "OFF"
        texte = self.textee(self.police, f"{p}% {etat}", couleur)
        fenetre.blit(texte, (x+int(40*self.echelle),y))
        pygame.draw.rect(fenetre, (30,40,30), (x+int(140*self.echelle),y+int(8*self.echelle),int(100*self.echelle),int(6*self.echelle)), border_radius=2)
        if p>0:
            pygame.draw.rect(fenetre, couleur, (x+int(140*self.echelle),y+int(8*self.echelle),int((p/100)*100*self.echelle),int(6*self.echelle)), border_radius=2)

    def oxygene(self, fenetre, joueur):
        largeur, hauteur = int(200*self.echelle), int(10*self.echelle)
        x,y = int(70*self.echelle), self.H-int(75*self.echelle)
        oxy = max(0, joueur.oxygene/joueur.oxygenemax)
        texteoxy = self.textee(self.policeoxy, "O²", BLEU)
        fenetre.blit(texteoxy, (x-int(40*self.echelle),y-int(6*self.echelle)))
        if oxy>0.3:
            couleur = BLEU
        elif oxy>0.1:
            couleur = ORANGE
        else:
            couleur = ROUGE
        pygame.draw.rect(fenetre, (20,30,20), (x, y, largeur, hauteur), border_radius=3)
        largeurbarre = int(oxy*largeur)
        if largeurbarre>0:
            pygame.draw.rect(fenetre, couleur, (x, y, largeurbarre, hauteur), border_radius=3)
        pygame.draw.rect(fenetre,(60,100,140), (x, y, largeur, hauteur),1, border_radius=3)
        if oxy <= 0 and pygame.time.get_ticks()%800<400:
            alerte = self.textee(self.policeoxy, "ASPHYXIE", ROUGE)
            fenetre.blit(alerte, alerte.get_rect(center=(int(160*self.echelle), int(self.H-int(170*self.echelle)))))

    def hud_life(self, fenetre, hp_cur, hp_max):
        x,y = int(20*self.echelle), self.H-int(45*self.echelle)
        rectnb = 20
        rectL, rectH = int(8*self.echelle), int(18*self.echelle)
        rectpos = int((hp_cur/hp_max)*rectnb)
        if hasattr(self, 'coeur'):
            fenetre.blit(self.coeur, (x,y-int(4*self.echelle)))
        for i in range(rectnb):
            rectposx = x+int(30*self.echelle)+(i*(rectL+int(2*self.echelle)))
            couleur = VERTPHOSPHORE if i < rectpos else (40,55,45)
            pygame.draw.rect(fenetre, couleur, (rectposx, y, rectL, rectH))
        textehp = self.textee(self.police, f"{int(hp_cur)}", VERTECLAT)
        fenetre.blit(textehp, (x+int(45*self.echelle)+(rectnb*int(10*self.echelle)), y-int(4*self.echelle)))

    def inventairedessin(self, fenetre, joueur, pos, clique, cliquedroit = False):
        img = assets.ASSETS.get("mode_inventaire")
        rect = img.get_rect(center=(self.L//2, self.H//2))
        fenetre.blit(img, rect)
        colonne = 3
        taille = int(200*self.echelle)
        mx = int(20*self.echelle)
        my = int(20*self.echelle)
        sx = rect.x+int(80*self.echelle)
        sy = rect.y+int(80*self.echelle)
        police = pygame.font.Font("ressource/police.ttf", max(16, int(22*self.echelle)))
        action = None
        #Cree les 9 cases
        for i, case in enumerate(joueur.inventaire):
            col = i%colonne
            ligne = i//colonne
            casex = sx + col*(taille+mx)
            casey = sy + ligne*(taille+my)
            rectcase = pygame.Rect(casex, casey, taille, taille)
            #Souris sur la case
            if rectcase.collidepoint(pos):
                #Contour quand on est dessus
                pygame.draw.rect(fenetre, (255,215,0), rectcase, 3, border_radius=5)
                if cliquedroit and case["type"] is not None:
                    action = ("DROP", i)
            #Affiche l'item
            if case["type"] is not None:
                nom = f"img_{case['type']}"
                imgitem = assets.ASSETS.get(nom)
                if imgitem:
                    imgitem = pygame.transform.scale(imgitem, (taille-45, taille-45))
                    rectitem = imgitem.get_rect(center=rectcase.center)
                    fenetre.blit(imgitem, rectitem)
                #aFFICGE NB QUE QUAND >1
                if case["quantite"] > 1:
                    masque = police.render(str(case["quantite"]), True, (0,0,0))
                    fenetre.blit(masque, (rectcase.right-24, rectcase.bottom-24))
                    #Texte
                    txt = police.render(str(case["quantite"]), True, (255,255,255))
                    fenetre.blit(txt, (rectcase.right-25, rectcase.bottom-25))
        return action