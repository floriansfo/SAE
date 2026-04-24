import pygame


TEXTE = (255,255,255)
GRIS = (180,180,180)
ROUGE = (200,60,60)
VERT = (80,200,80)

class Sommeil:
    def __init__(self, largeur, hauteur):
        self.L = largeur
        self.H = hauteur
        self.fonttitre = pygame.font.Font("ressource/titre.ttf", 36)
        self.fonttexte = pygame.font.Font("ressource/police.ttf", 22)
        self.ombre = pygame.Surface((self.L, self.H)).convert()
        self.ombre.fill((0,0,0))
        self.cours = False
        self.mode = "REPOS"
        self.time = 0
        self.alpha = 0
        self.jouractuel = 0
        self.soinpris = 0

    def update(self, L, H):
        self.L = L
        self.H = H
        self.ombre = pygame.Surface((self.L, self.H)).convert()
        self.ombre.fill((0,0,0))
    
    def dodo(self, joueur, jour, heure):
        if self.cours:
            return
        self.cours = True
        self.time = pygame.time.get_ticks()
        if heure <20:
            self.mode = "ERREUR"
        else:
            self.mode = "FONDU"
            self.alpha = 0
            self.jouractuel = jour
            soin = int(joueur.hpmax*0.30)
            self.soinpris = min(soin, joueur.hpmax-joueur.hp)
    
    def dessine(self, ecran, joueur):
        if not self.cours:
            return "RIEN"
        #Resolition
        resl, resh = ecran.get_size()
        if resl != self.L or resh != self.H:
            self.update(resl, resh)
        temps = pygame.time.get_ticks() - self.time
        if self.mode == "ERREUR":
            if temps < 1500:
                msg = self.fonttexte.render("Il n'est pas encore 20h", True, ROUGE)
                fond = pygame.Surface((msg.get_width()+40, msg.get_height()+20), pygame.SRCALPHA)
                fond.fill((0,0,0,200))
                fondrect = fond.get_rect(center=(self.L//2, self.H//2))
                ecran.blit(fond, fondrect)
                ecran.blit(msg, msg.get_rect(center=(self.L//2, self.H//2)))
                return "ENCOURS"
            else:
                self.cours = False
                return "ECHEC"
        elif self.mode == "FONDU":
            self.alpha += 5
            if self.alpha >= 255:
                self.alpha = 255
                self.mode = "TEXTE"
                self.time = pygame.time.get_ticks()
            self.ombre.set_alpha(self.alpha)
            ecran.blit(self.ombre,(0,0))
            return "ENCOURS"
        elif self.mode == "TEXTE":
            if temps < 2000:
                ecrannuit = pygame.Surface((self.L, self.H))
                ecrannuit.fill((0,0,0))
                y = self.H//2-90
                titre = self.fonttitre.render(f"NUIT du {self.jouractuel} au {self.jouractuel+1}", True, TEXTE)
                ecrannuit.blit(titre, titre.get_rect(center = (self.L//2,y)))
                y+=60
                #Separation ligne
                pygame.draw.line(ecrannuit, (60,60,80), (self.L//2-200, y),(self.L//2+200,y),1)
                y+=20
                #Text oxy
                oxytxt = self.fonttexte.render("Bouteille d'oxygene recharge", True, VERT)
                ecrannuit.blit(oxytxt, oxytxt.get_rect(center = (self.L//2,y)))
                y+=40
                #Text soin
                sointxt = self.fonttexte.render(f"Recuperation de {self.soinpris} HP", True, VERT)
                ecrannuit.blit(sointxt, sointxt.get_rect(center = (self.L//2,y)))
                ecran.blit(ecrannuit,(0,0))
                return "ENCOURS"
            else:
                 self.cours = False
                 return "REVEIL"