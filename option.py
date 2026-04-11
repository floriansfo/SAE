import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

pygame.init()
ecran = pygame.display.Info()
taille = (ecran.current_w, ecran.current_h)

#Bouton option
class Button:
    def __init__(self, text, x, y, w, h, action=None):
        self.rect = pygame.Rect(x, y, w, h) #Rectangle du bouton
        self.text = text #Texte du bouton
        self.action = action #Action lors du clic
        self.hover = False #Survol du bouton
        self.txtsurf = None
        self.txtrect = None
        self.fondtransparent = None
    
    def update_pos(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def update_cache(self, font):
        self.txtsurf = font.render(self.text, True, WHITE)
        self.txtrect = self.txtsurf.get_rect(center=self.rect.center)
        self.fondtransparent = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(self.fondtransparent,(0,0,0,150),(0,0,self.rect.width,self.rect.height), border_radius=10)
        
    def draw(self, surface):
        #Couleur du bouton au survol
        if self.hover:
            dessus = GOLD 
        else:
            dessus = BLACK
        #Transparence
        if self.fondtransparent:
            surface.blit(self.fondtransparent, self.rect.topleft)
        #Bordure du bouton
        pygame.draw.rect(surface, dessus, self.rect,2, border_radius=10)
        #Texte du bouton
        if self.txtsurf:
            surface.blit(self.txtsurf, self.txtrect)

    def is_clicked(self, pos,clique):
        #Verirife si cliqué et survolé
        self.hover = self.rect.collidepoint(pos)
        return self.hover and clique
    
#Barre régalage volume
class VolumeBar:
    def __init__(self, x, y, w, volume=0.5):
        self.rect = pygame.Rect(x, y, w, 10) #Rectangle de la barre
        self.volume = volume #Volume Actuelle
        self.cerclex = x+(w*volume) #Position de la boule
        self.cercley = y + 5 #Position verticale de la boule
        self.dragging = False #Indique si la poignée se déplace

    def repositionner(self, x, y):
        self.rect.x= x
        self.rect.y = y
        self.cercley = y + 5 #Position verticale de la boule
        self.cerclex = self.rect.x + (self.rect.width * self.volume) #Position de la boule en x

    def draw(self, surface):
        #Fond de la barre
        pygame.draw.rect(surface,(100,100,100),self.rect, border_radius=5)
        #Dessine la barre de volume remplie
        taillecouleur = max(1, self.cerclex - self.rect.x)
        couleur = pygame.Rect(self.rect.x, self.rect.y, taillecouleur, 10)
        pygame.draw.rect(surface, GOLD, couleur, border_radius=5)
        #Dessine la boule
        pygame.draw.circle(surface, WHITE, (int(self.cerclex), int(self.cercley)), 10)
        pygame.draw.circle(surface, GOLD, (int(self.cerclex), int(self.cercley)), 10,2)

    def actualise(self, pos, clique):
        #position entre souris et boule
        position = ((pos[0] - self.cerclex) ** 2 + (pos[1] - self.cercley) ** 2) ** 0.5
        #Vérifie si la boule est cliquée ou la barre
        if clique:
            if self.rect.collidepoint(pos) or position < 15:
                self.dragging = True #Glisser la boule
        else:
            self.dragging = False #clique relâché

        #si on glisse
        if self.dragging:
            #bloque la boule dans la barre
            self.cerclex = max(self.rect.x, min(pos[0], self.rect.right))
            #Met à jour le volume en fonction de la pos de la boule
            self.volume = (self.cerclex - self.rect.x) / self.rect.width
            return self.volume
        return None
    
#Boucle du menu option
def option_menu(fenetre, largeur, hauteur):
    clock = pygame.time.Clock()
    fonttitle = pygame.font.SysFont(None, 60)
    fonttext = pygame.font.SysFont(None, 30)

    L,H = fenetre.get_size()
    pleinecran = (fenetre.get_flags() & pygame.FULLSCREEN) != 0

    #Charge image de fond
    imgori = pygame.image.load("ressource/option.png").convert()
    imgfond = pygame.transform.scale(imgori, (L, H))

    #Créer les boutons
    #Bouton plein écran
    btn_pleinecran = Button("MODE: FENETRE", 0,0,300,50)
    if pleinecran:
        btn_pleinecran.text = "MODE: PLEIN ECRAN"
    #Bouton Résolution
    resolutions = [(1280,720),(1600,900),(1920,1080),(1920,1200),(2560,1440),(2560,1600),(3840,2160)]
    index = 0 #Index de la résolution premiere
    #Trouve l'index de la résolution actuelle
    if (L,H) in resolutions:
        index = resolutions.index((L,H))
    btn_resolution = Button(f"RESOLUTION: {L}x{H}", 0,0,300,50)
    #Barre de volume
    volumeactuel = pygame.mixer.music.get_volume()
    if volumeactuel > 0:
        posboule = volumeactuel ** (2/3)
    else:
        posboule = 0
    volume_barre = VolumeBar(0,0,300,posboule)
    #Bouton retour
    btn_retour = Button("RETOUR",0,0, 200, 50)
    titre_surf = None
    titre_rect = None
    txtpleinecran = None
    txtpleinecranrect = None
    barrevolume = None
    barrevolumerect = None
    panneau_surf = None
    panneau_rect = None

    def update_dimensions(newlargeur, newhauteur):
        nonlocal imgfond, titre_surf, titre_rect, txtpleinecran, txtpleinecranrect
        nonlocal barrevolume, barrevolumerect, panneau_surf, panneau_rect
        imgfond = pygame.transform.scale(imgori, (newlargeur, newhauteur))
        #Texte se regle en fonction de la res
        taille_titre = max(30, int(newhauteur*0.08))
        taille_texte = max(15, int(newhauteur*0.03))
        fonttitle = pygame.font.Font("ressource/titre.ttf", taille_titre)
        fonttext = pygame.font.Font("ressource/police.ttf", taille_texte)
        #Bouton se regle en fontion de res
        btnw = max(250, int(newlargeur*0.35))
        btnh = max(40, int(newhauteur*0.07))
        center_x = newlargeur // 2 - btnw//2
        #Positionnement des boutons
        btn_pleinecran.update_pos(center_x, int(newhauteur*0.18), btnw, btnh)
        btn_pleinecran.text = "MODE: PLEIN ECRAN" if pleinecran else "MODE: FENETRE"
        btn_pleinecran.update_cache(fonttext)

        btn_resolution.update_pos(center_x, int(newhauteur*0.28), btnw, btnh)
        btn_resolution.text = f"RESOLUTION: {newlargeur}x{newhauteur}"
        btn_resolution.update_cache(fonttext)
  
        txtpleinecran = fonttext.render("RESOLUTION DESACTIVE", True, (100,100,100))
        txtpleinecranrect = txtpleinecran.get_rect(center=(newlargeur//2, int(newhauteur*0.28)+btnh//2))

        barrevolume = fonttext.render("VOLUME MUSIQUE", True, WHITE)
        barrevolumerect = barrevolume.get_rect(midbottom=(newlargeur//2, int(newhauteur*0.43)))
        volume_barre.rect.width = btnw
        volume_barre.repositionner(center_x, int(newhauteur*0.45))

        #Panneau touche
        tabw = max(350, int(newlargeur*0.35))
        tabh = max(250, int(newhauteur*0.40))
        panneau_rect = pygame.Rect(newlargeur//2 - tabw//2, int(newhauteur*0.55), tabw, tabh)

        panneau_surf = pygame.Surface((tabw, tabh), pygame.SRCALPHA)
        pygame.draw.rect(panneau_surf, (50,50,50), (0,0,tabw,tabh), border_radius=15)
        pygame.draw.rect(panneau_surf, GOLD, (0,0,tabw,tabh), 2, border_radius=15)

        commande = ["COMMANDES DU JEU:", "AVANCER: Z", "RECULER: S", "GAUCHE: Q", "DROITE: D", "PAUSE: ECHAP", "LUMIERE: H", "FILTRE: T", "ARME: 1,2,3", "TIR:CLIQUE GAUCHE"]
        espacement = tabh // (len(commande)+1)
        #Ecris dans le tab
        for i, ligne in enumerate(commande):
            titre_couleur = GOLD if i == 0 else WHITE
            texte = fonttext.render(ligne, True, titre_couleur)
            panneau_surf.blit(texte, (tabw//2 - texte.get_width()//2, 10+(i*espacement)))
    
        btn_retour.update_pos(int(newlargeur*0.05), newhauteur-btnh-int(newhauteur*0.05), max(150, int(newlargeur*0.15)), btnh)
        btn_retour.update_cache(fonttext)

        titre_surf = fonttitle.render("OPTIONS", True, WHITE)
        titre_rect = titre_surf.get_rect(midtop=(newlargeur//2, int(newhauteur*0.05)))

    imgfond = None
    update_dimensions(L,H)

    running = True
    while running:
        pos = pygame.mouse.get_pos()
        clique = False
        actionclique = pygame.mouse.get_pressed()[0]
        #Gestion de clique
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clique = True
            #Resize de l'écran
            if event.type == pygame.VIDEORESIZE:
                if not pleinecran:
                    L,H = event.w, event.h
                    fenetre = pygame.display.set_mode((L,H), pygame.RESIZABLE)
                    update_dimensions(L,H)
        #Bouton plein écran
        if btn_pleinecran.is_clicked(pos, clique):
            pleinecran = not pleinecran
            if pleinecran:
                #Si mode plein écran on passe a la résolution de l'ecran
                fenetre = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            else:
                #Si mode fenetre on passe a cette résolution
                fenetre = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
            L,H = fenetre.get_size()
            update_dimensions(L,H)
        #Bouton résolution
        if not pleinecran and btn_resolution.is_clicked(pos, clique):
                #Change la résolution par la suivante de la liste
                index = (index + 1) % len(resolutions)
                new_res = resolutions[index]
                fenetre = pygame.display.set_mode(new_res, pygame.RESIZABLE)
                L,H = new_res
                update_dimensions(L,H)
        #Clique ou non sur la barre de volume
        nouveau_volume = volume_barre.actualise(pos, actionclique)
        if nouveau_volume is not None:
            pygame.mixer.music.set_volume(nouveau_volume**1.5) #Volume pour un volume plus rapide
        #Clique sur le bouton retour
        if btn_retour.is_clicked(pos, clique):
            running = False
        fenetre.blit(imgfond, (0, 0))
        #Affiche le mot "Options"
        fenetre.blit(titre_surf, titre_rect)
        #Dessine les boutons
        btn_pleinecran.draw(fenetre)
        if not pleinecran:
            btn_resolution.draw(fenetre)
        else:
            #En plein ecran on met Resolution désactivée
            fenetre.blit(txtpleinecran, txtpleinecranrect)
        #Dessine la barre de volume
        fenetre.blit(barrevolume, barrevolumerect)
        volume_barre.draw(fenetre)
        #Dessine panneau
        fenetre.blit(panneau_surf, panneau_rect)
        btn_retour.draw(fenetre)
        pygame.display.flip()
        clock.tick(60)
    return fenetre