import pygame
import os

VERTFOND = (10,25,15,210)
VERTBORD = (45,90,55)
VERTPHOSPHORE = (100,255,150)
VERTECLAT = (180,255,200)
BLANC = (240,255,240)
ROUGE = (255,60,60)
ORANGE =(255,170,50)
NOIRTRANSPARENT = (0,0,0,160)

ARTICLE = [{"id": 1, "nom": "Pistolet", "prix": 80, "description": "Arme de base", "type": "arme" },
           {"id": 2,     "nom": "Fusil a pompe",  "prix": 150, "description": "5 balles, puissant, cadence faible", "type": "arme"},
           {"id": 3,     "nom": "Fusil d'assaut", "prix": 250, "description": "Rapide, attention au recul",         "type": "arme"},
           {"id": "pile", "nom": "Pile lampe",    "prix": 50,  "description": "Recharge pile lampe",                "type": "pile"},
           {"id": "lampe","nom": "Lampe torche",  "prix": 100, "description": "Permet de s'eclairer",               "type": "lampe"},]

PRIXNIVEAU = {2: 100, 3:200, 4:350, 5:500, 6:750}

class Boutique:
    def __init__(self, largeur, hauteur):
        self.L = largeur
        self.H = hauteur
        self.titre = pygame.font.Font("ressource/fonts/titre.ttf", 32)
        self.normal = pygame.font.Font("ressource/fonts/police.ttf", 20)
        self.petit = pygame.font.Font("ressource/fonts/police.ttf", 16)
        self.cache()
        
    def update(self, L, H):
        self.L = L
        self.H = H
        self.cache()
    
    def cache(self):
        self.menuL = min(700, self.L-60)
        self.menuH = min(720, self.H-60)
        self.PUSH = 20
        self.ligne = 60
        self.w = self.menuL-self.PUSH*2

        #Fond boutique
        self.fond = pygame.Surface((self.menuL, self.menuH), pygame.SRCALPHA)
        pygame.draw.rect(self.fond, VERTFOND, (0,0,self.menuL,self.menuH), border_radius=6)
        pygame.draw.rect(self.fond, VERTBORD, (0,0,self.menuL,self.menuH), 2, border_radius=6)
        #Coin lumineu
        pygame.draw.line(self.fond, VERTPHOSPHORE, (0,15), (0, 30), 4)
        pygame.draw.line(self.fond, VERTPHOSPHORE, (15,0), (30, 0), 4)
        #Texte
        self.txttitre = self.titre.render("BOUTIQUE D'EQUIPEMENT", True, VERTPHOSPHORE)
        self.partarm = self.petit.render("ARMEMENT ET SURVIE", True, VERTBORD)
        self.partetage= self.petit.render("NIVEAU D'ETAGE", True, VERTBORD)
        self.touche = self.petit.render("CLIC GAUCHE: ACQUERIR | E: FERMER", True, VERTBORD)

        #Bouton
        self.boutonnorm = pygame.Surface((self.w,self.ligne), pygame.SRCALPHA)
        pygame.draw.rect(self.boutonnorm, (15,30,20,180), (0,0,self.w,self.ligne), border_radius=4)
        pygame.draw.rect(self.boutonnorm, VERTBORD, (0,0,self.w,self.ligne), 1, border_radius=4)
        self.boutondessus = pygame.Surface((self.w,self.ligne), pygame.SRCALPHA)
        pygame.draw.rect(self.boutondessus, VERTECLAT, (0,0,self.w,self.ligne), border_radius=4)
        pygame.draw.rect(self.boutondessus, VERTPHOSPHORE, (0,0,self.w,self.ligne), 1, border_radius=4)
        self.boutonutilise = pygame.Surface((self.w,self.ligne), pygame.SRCALPHA)
        pygame.draw.rect(self.boutonutilise, (10,15,10,120), (0,0,self.w,self.ligne), border_radius=4)
        pygame.draw.rect(self.boutonutilise, (30,50,30), (0,0,self.w,self.ligne), 1, border_radius=4)
        #Texte article
        self.cachearticle = {}
        for art in ARTICLE:
            nom = self.normal.render(art["nom"], True, BLANC)
            description = self.petit.render(art["description"], True, (130,160,140))
            self.cachearticle[art["id"]] = (nom, description)
        #Bouton niveau
        nbniv = len(PRIXNIVEAU)
        self.btnw = (self.w-(nbniv-1)*10)//nbniv
        self.btnh = 45
        self.surfnorm = pygame.Surface((self.btnw,self.btnh), pygame.SRCALPHA)
        pygame.draw.rect(self.surfnorm, (15,30,20,180), (0,0,self.btnw,self.btnh), border_radius=4)
        pygame.draw.rect(self.surfnorm, VERTBORD, (0,0,self.btnw,self.btnh), 1, border_radius=4)
        self.surfdessus = pygame.Surface((self.btnw,self.btnh), pygame.SRCALPHA)
        pygame.draw.rect(self.surfdessus, VERTECLAT, (0,0,self.btnw,self.btnh), border_radius=4)
        pygame.draw.rect(self.surfdessus, VERTPHOSPHORE, (0,0,self.btnw,self.btnh), 1, border_radius=4)
        self.surutilise = pygame.Surface((self.btnw,self.btnh), pygame.SRCALPHA)
        pygame.draw.rect(self.surutilise, (20,65,30,180), (0,0,self.btnw,self.btnh), border_radius=4)
        pygame.draw.rect(self.surutilise, VERTPHOSPHORE, (0,0,self.btnw,self.btnh), 1, border_radius=4)

    def dessiner(self, ecran, joueur, nb_joueur=1):
        #Resolution
        resl, resh = ecran.get_size()
        if resl != self.L or resh != self.H:
            self.update(resl, resh)
        #Fond noir
        fond = pygame.Surface((self.L, self.H), pygame.SRCALPHA)
        fond.fill(NOIRTRANSPARENT)
        ecran.blit(fond, (0,0))
        #Position
        x = (self.L-self.menuL)//2
        y = (self.H-self.menuH)//2
        #Fond et titre
        ecran.blit(self.fond, (x,y))
        ecran.blit(self.txttitre, self.txttitre.get_rect(center=(x+self.menuL//2, y+35)))
        pygame.draw.line(ecran, VERTBORD, (x+self.PUSH, y+65), (x+self.menuL-self.PUSH, y+65),2)
        #Texte
        limite = 2 if nb_joueur <= 2 else 3
        restant = max(0, limite-joueur.achatjour)
        solde = self.normal.render(f"PIECES: {joueur.pieces}", True, ORANGE)
        ecran.blit(solde, (x+self.PUSH, y+80))
        couleurreste = VERTPHOSPHORE if restant > 0 else ROUGE
        txtachat = self.petit.render(f"ACHATS RESTANTS: {restant}/{limite}", True, couleurreste)
        ecran.blit(txtachat, txtachat.get_rect(topright=(x+self.menuL-self.PUSH, y+85)))
        #Partie article
        posy = y+105
        ecran.blit(self.partarm, (x+self.PUSH, posy))
        posy+=22
        boutons = []
        mouse = pygame.mouse.get_pos()
        for article in ARTICLE:
            ay = posy
            artrect = pygame.Rect(x+self.PUSH, ay, self.w, self.ligne)
            arttype = article["type"]
            deja = (joueur.arsenal_achete.get(article["id"], False) if arttype == "arme" else joueur.possedelampe if arttype == "lampe" else False)
            peut = joueur.pieces >= article["prix"] and restant >0 and not deja
            dessus = artrect.collidepoint(mouse) and peut
            #Dessin
            if deja and arttype != "pile":
                ecran.blit(self.boutonutilise, artrect.topleft)
            elif dessus:
                ecran.blit(self.boutondessus, artrect.topleft)
            else:
                ecran.blit(self.boutonnorm, artrect.topleft)
            #Texte
            nom, description = self.cachearticle[article["id"]]
            ecran.blit(nom, (artrect.x+15, artrect.y+12))
            ecran.blit(description, (artrect.x+15, artrect.y+40))
            #Status achat
            if deja and arttype != "pile":
                etat = self.normal.render("ACQUIS", True, VERTBORD)
                ecran.blit(etat, etat.get_rect(midright=(artrect.right-20, artrect.centery)))
            else:
                couleurprix = VERTPHOSPHORE if peut else ROUGE
                prix = self.normal.render(f"{article['prix']}P", True, couleurprix)
                ecran.blit(prix, prix.get_rect(midright = (artrect.right-20, artrect.centery)))
                boutons.append((artrect, article))
            posy+=self.ligne+6
        posy +=5
        pygame.draw.line(ecran, VERTBORD, (x+self.PUSH, posy), (x+self.menuL-self.PUSH, posy),2)
        posy +=15
        ecran.blit(self.partetage, (x+self.PUSH, posy))
        
        #malachite trade
        malachite_tt=0
        for case in joueur.inventaire:
            if case["type"]=="minerai":
                malachite_tt+=case["quantite"]
        artrect = pygame.Rect(x+self.PUSH, posy, self.w, self.ligne)
        dessus = artrect.collidepoint(mouse) and malachite_tt>0
        if dessus:
            ecran.blit(self.boutondessus, artrect.topleft)
        else:
            ecran.blit(self.boutonnorm, artrect.topleft)
        nom= self.normal.render(f"Malachite x{malachite_tt}", True, BLANC)
        description= self.petit.render("Echanger contre des pieces", True, (130, 160, 140))
        ecran.blit(nom, (artrect.x+15, artrect.y+12))
        ecran.blit(description, (artrect.x+15, artrect.y+40))
        couleurprix = VERTPHOSPHORE if malachite_tt>0 else ROUGE
        prix = self.normal.render(f"+{malachite_tt*30}P", True, couleurprix)
        ecran.blit(prix, prix.get_rect(midright = (artrect.right-20, artrect.centery)))
        boutons.append((artrect, {"id":"malachite", "prix":0, "type":"malachite"}))
        posy+=self.ligne+6
        posy+=30
        #Partie Niveaux
        for idd, (niveau, prix) in enumerate(PRIXNIVEAU.items()):
            posx = x+self.PUSH+idd*(self.btnw+10)
            btnrect = pygame.Rect(posx, posy, self.btnw, self.btnh)
            debloque = niveau in joueur.niveaudebloque
            ordre = (niveau==2) or ((niveau-1) in joueur.niveaudebloque)
            peu = joueur.pieces >= prix and restant>0 and not debloque and ordre
            dessuss = btnrect.collidepoint(mouse) and peu
            #Dessin
            if debloque:
                ecran.blit(self.surutilise, btnrect.topleft)
                txt = self.petit.render(f"OK {niveau}", True, VERTBORD)
            elif not ordre:
                ecran.blit(self.surfnorm, btnrect.topleft)
                txt = self.petit.render("BLOQUE", True, (120,120,120))
            else:
                if dessuss:
                    ecran.blit(self.surfdessus, btnrect.topleft)
                    couleurtexte = VERTPHOSPHORE
                else:
                    ecran.blit(self.surfnorm, btnrect.topleft)
                    couleurtexte = BLANC if peu else ROUGE
                txt = self.petit.render(f"NIVEAU {niveau} {prix}P", True, couleurtexte)
            ecran.blit(txt, txt.get_rect(center=btnrect.center))
            if not debloque and ordre:
                boutons.append((btnrect, {"id": f"niveau{niveau}", "prix": prix, "type": "niveau", "niveau": niveau}))
        #Texte commande
        ecran.blit(self.touche, self.touche.get_rect(center= (x+self.menuL//2, y+self.menuH-25)))
        return boutons
    

    
    def clique(self, mouse_pos, boutons, joueur, nb_joueur=1):
        limite = 2 if nb_joueur <= 2 else 3
        for rect, article in boutons:
            if not rect.collidepoint(mouse_pos):
                continue
            arttype = article["type"]
            if arttype != "malachite" and joueur.achatjour >= limite:
                return False
            if joueur.pieces < article["prix"]:
                return False
            if arttype == "arme":
                if joueur.arsenal_achete.get(article["id"], False):
                    return False
                joueur.pieces -= article["prix"]
                joueur.arsenal_achete[article["id"]] = True
                joueur.achatjour += 1
                if article["id"] == 1:
                    joueur.munition = 30
                return True
            elif arttype == "pile":
                joueur.pieces -= article["prix"]
                joueur.pile = joueur.pilemax
                joueur.achatjour += 1
                return True
            elif arttype == "lampe":
                if joueur.possedelampe:
                    return False
                joueur.pieces -= article["prix"]
                joueur.possedelampe = True
                joueur.pile = joueur.pilemax
                joueur.achatjour += 1
                if hasattr(joueur, "quantite"):
                    joueur.quantite("lampe", 1)
                return True
            elif arttype == "niveau":
                niv = article["niveau"]
                if niv in joueur.niveaudebloque:
                    return False
                if niv > 2 and (niv-1) not in joueur.niveaudebloque:
                    return False
                joueur.pieces -= article["prix"]
                joueur.niveaudebloque.add(niv)
                joueur.achatjour += 1
                return True
            elif arttype == "malachite":
                total = sum(case["quantite"] for case in joueur.inventaire if case["type"]=="minerai")
                if total<=0:
                    return False
                joueur.pieces += total*30
                for case in joueur.inventaire:
                    if case["type"]=="minerai":
                        case["quantite"]=0
                        case["type"] = None
                return True
        return False