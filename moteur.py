import pygame

#Couleur 
VERTFOND = (10,25,15,240)
VERTBORD = (45,90,55)
VERTPHOSPHORE = (100,255,150)
ROUGE = (255,60,60)
ORANGE =(255,170,50)
BLANC = (255,255,255)

class Moteur:
    def __init__(self, largeur, hauteur):
        self.L = largeur
        self.H = hauteur
        self.texte = pygame.font.Font("ressource/police.ttf", 20)
        self.titre = pygame.font.Font("ressource/police.ttf", 30)
        self.moteur = pygame.Rect(self.L//2-350, self.H//2-200, 450,400)
        self.trou = pygame.Rect(self.L//2-200, self.H//2-60, 120, 120)
        self.inventaire = pygame.Rect(self.L//2+150, self.H//2-100, 200,200)
        self.cristal = pygame.Rect(self.L//2+190, self.H//2+60, 120,120)
        self.cristalpos = self.cristal.topleft
        #Glisse depose
        self.attrape = False
        self.pox = 0
        self.poy = 0
        #Resolu
        self.estla = False
        self.resolu = False
    
    def gerer_evenements(self, event, joueur):
        if self.resolu:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #Clic gauche
                if joueur.cristal and not self.estla and self.cristal.collidepoint(event.pos):
                    self.attrape = True
                    mx,my = event.pos
                    self.pox = self.cristal.x - mx
                    self.poy = self.cristal.y - my
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.attrape:
                self.attrape = False
                #Vérifie si le cristal est dans le trou
                x = self.cristal.centerx - self.trou.centerx
                y = self.cristal.centery - self.trou.centery
                dist = (x**2 + y**2)**0.5
                if dist < 60:
                    #Le cristal est dans le trou
                    self.cristal.center = self.trou.center
                    self.estla = True
                    self.victoire(joueur)
                else:
                    self.cristal.topleft = self.cristalpos
        elif event.type == pygame.MOUSEMOTION:
            if self.attrape:
                mx,my = event.pos
                self.cristal.x = mx + self.pox
                self.cristal.y = my + self.poy
    
    def victoire(self, joueur):
        if getattr(joueur, "a_tango", False):
            self.resolu = True

    def dessiner(self, fenetre, joueur, imgcristal = None):
        #Fond
        fond = pygame.Surface((self.L, self.H), pygame.SRCALPHA)
        fond.fill((0,0,0,200))
        fenetre.blit(fond, (0,0))
        #Dessin moteur
        pygame.draw.rect(fenetre, VERTFOND, self.moteur, border_radius=10)
        pygame.draw.rect(fenetre, VERTBORD, self.moteur, width=3, border_radius=10)
        titre = self.titre.render("REACTEUR VAISSEAU", True, VERTPHOSPHORE)
        fenetre.blit(titre, (self.moteur.x+20 , self.moteur.y + 20))
        couleur = VERTPHOSPHORE if self.estla else VERTBORD
        pygame.draw.rect(fenetre, couleur, self.trou, 2, border_radius=5)
        #Dessin parti a droite inventaire
        pygame.draw.rect(fenetre, VERTFOND, self.inventaire, border_radius=10)
        pygame.draw.rect(fenetre, VERTBORD, self.inventaire, 3, border_radius=10)
        titreinv = self.texte.render("STOCKAGE", True, VERTBORD)
        fenetre.blit(titreinv, (self.inventaire.x+20, self.inventaire.y+20))
        #Dessin cristal
        if joueur.cristal:
            if imgcristal:
                if not hasattr(self, "imgcristalnouv"):
                    self.imgcristalnouv = pygame.transform.scale(imgcristal, (120,120))
                fenetre.blit(self.imgcristalnouv, self.cristal.topleft)
        #Texte
        if self.resolu:
            txt = self.font.render("SYSTEME ALIMENTE", True, VERTPHOSPHORE)
        elif not joueur.cristal:
            txt = self.texte.render("CRISTAL MANQUANT", True, ROUGE)
        elif not self.estla:
            txt = self.texte.render("INSEREZ LE CRISTAL", True, ORANGE)
        elif not getattr(joueur, "a_tango", False):
            txt = self.texte.render("TANGO DOIT ETRE AVEC TOI", True, ORANGE)
        fenetre.blit(txt, txt.get_rect(center=(self.L//2, self.H-100)))
        #Texte commande
        txtcommande = self.texte.render("Appuyer sur ECHAP pour fermer", True, VERTBORD)
        fenetre.blit(txtcommande, txtcommande.get_rect(center=(self.L//2, self.H-50)))