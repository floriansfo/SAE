import pygame

# Couleurs
INTERFACE = (50, 50, 50, 200)
TEXTE = (255, 255, 255)
BORDURE = (255, 255, 255)
BUTTON_HOVER = (100,200,100)
BUTTONACTUEL = (200, 100, 100)
NOIR_TRANSPARENT = (0, 0, 0, 180)

class Ascenseur:
    def __init__(self, fenterelarge, fenetrehaute):
        self.L = fenterelarge
        self.H = fenetrehaute
        self.update_dimensions(self.L, self.H)

    def update_dimensions(self, L, H):
        self.L = L
        self.H = H
        self.echelle = self.H/1080.0
        #police
        self.font = pygame.font.Font("ressource/fonts/police.ttf", max(12, int(18*self.echelle)))
        self.title = pygame.font.Font("ressource/fonts/police.ttf", max(18, int(31*self.echelle)))
        self.sous_titre = pygame.font.Font("ressource/fonts/police.ttf", max(14, int(21*self.echelle)))
        #taille menu
        self.menuL = int(240*self.echelle)
        self.menuH = int(380*self.echelle)
    
    def dessiner(self, ecran, niveau, joueur = None):
        rad = int(10*self.echelle)
        #Position du menu
        x = self.L - self.menuL - int(20*self.echelle)
        y = self.H - self.menuH - int(60*self.echelle)
        #Fond du menu
        menurect = pygame.Rect(x, y, self.menuL, self.menuH)
        menu = pygame.Surface((self.menuL, self.menuH), pygame.SRCALPHA)
        menu.fill(INTERFACE)
        ecran.blit(menu, (x, y))
        #Cadre autour du menu
        pygame.draw.rect(ecran, BORDURE, menurect, max(1, int(2*self.echelle)))
        #Titre du menu
        titre = self.sous_titre.render(f"ETAGE ACTUEL: {niveau}", True, TEXTE)
        #Centrer le titre dans le menu
        titre_rect = titre.get_rect(center=(x + self.menuL//2, y+int(40*self.echelle)))
        ecran.blit(titre, titre_rect)
        #Bouton pour monter d'etage
        mouse_pos = pygame.mouse.get_pos()
        bouton = []
        #Position du bouton
        btnx = int(20*self.echelle)
        btny = int(20*self.echelle)
        btnl = int(80*self.echelle)
        btnh = int(60*self.echelle)
        niveaudebloque = joueur.niveaudebloque if joueur else set(range(1,7))
        #Boucle pour crér les 6 boutons
        for i in range(1,7):
            col = (i-1)%2
            row = (i-1)//2
            #Position du bouton
            Positionx = x+int(30*self.echelle)+col*(btnl+btnx)
            Positiony = y+int(80*self.echelle)+row*(btnh+btny)
            bouton_rect = pygame.Rect(Positionx, Positiony, btnl, btnh)
            debloque = i in niveaudebloque
            if i == niveau:
                couleur = BUTTONACTUEL
            elif not debloque:
                couleur = (40,40,40,200)
            elif bouton_rect.collidepoint(mouse_pos):
                couleur = BUTTON_HOVER
            else:
                couleur = NOIR_TRANSPARENT
            #Afichage bouton
            pygame.draw.rect(ecran, couleur, bouton_rect, border_radius=rad)
            pygame.draw.rect(ecran, BORDURE if debloque or i == niveau else (80,80,80), bouton_rect, max(1, int(2*self.echelle)),border_radius=rad)
            if (debloque or i == niveau):
                couleur_texte = TEXTE 
            else:
                couleur_texte = (80,80,80)
            #Texte du bouton
            texte = self.font.render(f"NIVEAU {i}", True, couleur_texte)
            #Centrer le texte dans le bouton
            texte_rect = texte.get_rect(center=bouton_rect.center)
            ecran.blit(texte, texte_rect)
            if not debloque and i!= niveau:
                prix = {2: 100, 3: 200, 4: 350, 5: 500, 6: 750}.get(i, 999)
                prix_texte = self.font.render(f"{prix}p", True, (255,200,50))
                ecran.blit(prix_texte, prix_texte.get_rect(center=(bouton_rect.centerx, bouton_rect.bottom-int(14*self.echelle))))
            elif debloque and i != niveau:
                bouton.append((bouton_rect, i))
        #Bouton pour retourner au vaisseau
        btnvaisseau_rect =pygame.Rect(x+int(30*self.echelle), y+int(320*self.echelle), self.menuL-int(60*self.echelle), int(40*self.echelle))
        if niveau == 0:
            pygame.draw.rect(ecran, BUTTONACTUEL, btnvaisseau_rect, border_radius=rad)
        else:
            if btnvaisseau_rect.collidepoint(mouse_pos):
                couleur = BUTTON_HOVER 
            else:
                couleur = NOIR_TRANSPARENT
            pygame.draw.rect(ecran, couleur, btnvaisseau_rect, border_radius=rad)
            bouton.append((btnvaisseau_rect, 0))
        pygame.draw.rect(ecran, BORDURE, btnvaisseau_rect, max(1, int(2*self.echelle)),border_radius=rad)
        texte_vaisseau = self.font.render("VAISSEAU", True, TEXTE)
        ecran.blit(texte_vaisseau, texte_vaisseau.get_rect(center=btnvaisseau_rect.center))
        return bouton
    
    def clique(self, mouse_pos, boutons):
        for rect, etage in boutons:
            if rect.collidepoint(mouse_pos):
                return etage
        return None
    
    def ecran_charge(self, ecran, img, etagechoisis):
        #Ecran de chargement noir avec texte de chargement
        ecran.fill((0,0,0))
        #TEXTE DE CHARGEMENT
        texte = self.title.render(f"CHARGEMENT DE L'ETAGE {etagechoisis}...", True, TEXTE)
        texte_rect = texte.get_rect(center=(self.L//2, self.H//2))
        ecran.blit(texte, texte_rect)
        pygame.display.flip()
        pygame.event.pump()  # Traiter les événements pour éviter que la fenêtre ne se fige