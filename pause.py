import pygame
import os

NOIR_TRANSPARENT = (0, 0, 0, 180)
VERTFOND = (10,25,15,210)
VERTBORD = (45,90,55)
VERTPHOSPHORE = (100,255,150)
VERTECLAT = (20,50,30,240)
BLANC = (240,255,240)

class EcranPause:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        #Police
        police = os.path.join("ressource", "police.ttf")
        self.font_titre = pygame.font.Font(police, 60)
        self.font_option = pygame.font.Font(police, 30)
        #Definition boutons    
        self.buttons = [("REPRENDRE","Reprendre"),("OPTIONS","Options"),("SAUVEGARDER","Sauvegarder"),("MENU PRINCIPAL","Menu Principal"),("QUITTER","Quitter")]
        #Caracteristique des boutons
        self.btnLargeur = 300
        self.btnHauteur = 60
        self.espacement = 20
        self.cache()
    
    def update_dimensions(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.cache()
    
    def cache(self):
        #Fond trensparent
        self.fond = pygame.Surface((self.largeur, self.hauteur), pygame.SRCALPHA)
        self.fond.fill(NOIR_TRANSPARENT)
        #Titre
        self.txt = self.font_titre.render("PAUSE", True, VERTPHOSPHORE)
        self.txtrect = self.txt.get_rect(center=(self.largeur//2, self.hauteur//5))
        #Panneau des boutons
        self.surface = pygame.Surface((self.btnLargeur,self.btnHauteur), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, VERTFOND, (0,0,self.btnLargeur,self.btnHauteur), border_radius=4)
        pygame.draw.rect(self.surface, VERTBORD, (0,0,self.btnLargeur,self.btnHauteur), 2, border_radius=4)
        pygame.draw.line(self.surface, VERTPHOSPHORE, (0,6), (0, 16), 3)
        pygame.draw.line(self.surface, VERTPHOSPHORE, (6,0), (16, 0), 3)
        self.dessus = pygame.Surface((self.btnLargeur,self.btnHauteur), pygame.SRCALPHA)
        pygame.draw.rect(self.dessus, VERTECLAT, (0,0,self.btnLargeur,self.btnHauteur), border_radius=4)
        pygame.draw.rect(self.dessus, VERTPHOSPHORE, (0,0,self.btnLargeur,self.btnHauteur), 2, border_radius=4)
        pygame.draw.line(self.dessus, BLANC, (0,6), (0, 16), 3)
        pygame.draw.line(self.dessus, BLANC, (6,0), (16, 0), 3)
        self.btn=[]
        hauteurboutons = len(self.buttons) * self.btnHauteur + (len(self.buttons) - 1)*self.espacement
        debut = (self.hauteur - hauteurboutons)// 2
        if debut<self.txtrect.bottom+30:
            debut = self.txtrect.bottom+30
        x = (self.largeur - self.btnLargeur) // 2
        for i, (key, text) in enumerate(self.buttons):
            y = debut + i * (self.btnHauteur + self.espacement)
            rect = pygame.Rect(x, y, self.btnLargeur, self.btnHauteur)
            txt = self.font_option.render(text, True, VERTBORD)
            txtdessus = self.font_option.render(text, True, VERTPHOSPHORE)
            txtrect = txt.get_rect(center=rect.center)
            self.btn.append((rect,key,txt,txtdessus,txtrect))
    
    def dessiner(self, fenetre):
        #Fond semi transparent
        fenetre.blit(self.fond, (0,0))
        #Titre
        fenetre.blit(self.txt, self.txtrect)
        mouse_pos = pygame.mouse.get_pos()
        rectbtn = []
        #Affiche les boutons
        for rect, key, txt, txtdessus, txtrect in self.btn:
            if rect.collidepoint(mouse_pos):
                fenetre.blit(self.dessus, rect.topleft)
                fenetre.blit(txtdessus, txtrect)
            else:
                fenetre.blit(self.surface, rect.topleft)
                fenetre.blit(txt, txtrect)
            rectbtn.append((rect, key))
        return rectbtn

    def clique(self, mouse_pos, rectbtn):
        #On parcours la liste de dessiner()
        for rect, action in rectbtn:
            #Si coordonnée sont dans un rectangle
            if rect.collidepoint(mouse_pos):
                return action #Renvoie vers l'utilité du bouton 
        return None
        