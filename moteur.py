import pygame

# --- PALETTE TACTIQUE ---
VERT_FOND = (10, 25, 15, 240)
VERT_BORD = (45, 90, 55)
VERT_PHOSPHORE = (100, 255, 150)
ROUGE_ALERTE = (255, 60, 60)
ORANGE_TACTIQUE = (255, 170, 50)
BLANC = (255, 255, 255)

class PuzzleMoteur:
    def __init__(self, largeur, hauteur):
        self.L = largeur
        self.H = hauteur
        self.font = pygame.font.Font("ressource/police.ttf", 20)
        self.font_titre = pygame.font.Font("ressource/police.ttf", 30)

        # --- ZONES DE L'INTERFACE ---
        # Le grand bloc à gauche (Le Moteur)
        self.rect_moteur = pygame.Rect(self.L//2 - 350, self.H//2 - 200, 450, 400)
        # L'emplacement exact où placer le cristal dans le moteur
        self.rect_slot = pygame.Rect(self.L//2 - 200, self.H//2 - 60, 120, 120)

        # Le petit bloc à droite (L'Inventaire)
        self.rect_inv = pygame.Rect(self.L//2 + 150, self.H//2 - 100, 200, 200)

        # L'objet à déplacer (Cristal/Diamant)
        self.rect_cristal = pygame.Rect(self.L//2 + 190, self.H//2 - 60, 120, 120)
        self.cristal_base_pos = self.rect_cristal.topleft # Mémoire de sa position de départ

        # Paramètres de Glisser-Déposer
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        
        # Statut du puzzle
        self.en_place = False
        self.resolu = False

    def gerer_evenements(self, event, joueur):
        if self.resolu:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic gauche
                # On ne peut l'attraper que si le joueur le possède, qu'il n'est pas déjà en place, et qu'on clique dessus
                if joueur.cristal and not self.en_place and self.rect_cristal.collidepoint(event.pos):
                    self.dragging = True
                    mouse_x, mouse_y = event.pos
                    # Calcule l'écart entre le clic et le coin de l'objet pour un déplacement fluide
                    self.offset_x = self.rect_cristal.x - mouse_x
                    self.offset_y = self.rect_cristal.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:
                self.dragging = False
                # Vérifier si on l'a lâché près du slot du moteur (Tolérance de 60 pixels)
                dx = self.rect_cristal.centerx - self.rect_slot.centerx
                dy = self.rect_cristal.centery - self.rect_slot.centery
                distance = (dx**2 + dy**2)**0.5

                if distance < 60: 
                    # Aimantation automatique (Snapping)
                    self.rect_cristal.center = self.rect_slot.center
                    self.en_place = True
                    self.verifier_victoire(joueur)
                else:
                    # Retour brusque à l'inventaire si on rate le trou
                    self.rect_cristal.topleft = self.cristal_base_pos

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect_cristal.x = mouse_x + self.offset_x
                self.rect_cristal.y = mouse_y + self.offset_y

    def verifier_victoire(self, joueur):
        # Le cristal est en place, a-t-on sauvé le soldat Tango ?
        # ATTENTION : Remplace "a_tango" par la variable que tu as créée dans ta classe Joueur pour savoir s'il a le soldat !
        if getattr(joueur, "a_tango", False): 
            self.resolu = True
            # La vidéo se lancera depuis jeu.py quand cette variable passera à True

    def dessiner(self, fenetre, joueur, image_cristal=None):
        # Fond sombre pour mettre en valeur le puzzle
        fond_noir = pygame.Surface((self.L, self.H), pygame.SRCALPHA)
        fond_noir.fill((0, 0, 0, 200))
        fenetre.blit(fond_noir, (0, 0))

        # 1. Dessin du Moteur (Gauche)
        pygame.draw.rect(fenetre, VERT_FOND, self.rect_moteur, border_radius=10)
        pygame.draw.rect(fenetre, VERT_BORD, self.rect_moteur, 3, border_radius=10)
        titre_m = self.font_titre.render("REACTEUR PRINCIPAL", True, VERT_PHOSPHORE)
        fenetre.blit(titre_m, (self.rect_moteur.x + 20, self.rect_moteur.y + 20))
        
        # Le "trou" du moteur
        couleur_slot = VERT_PHOSPHORE if self.en_place else VERT_BORD
        pygame.draw.rect(fenetre, couleur_slot, self.rect_slot, 2, border_radius=5)

        # 2. Dessin de l'Inventaire (Droite)
        pygame.draw.rect(fenetre, VERT_FOND, self.rect_inv, border_radius=10)
        pygame.draw.rect(fenetre, VERT_BORD, self.rect_inv, 3, border_radius=10)
        titre_i = self.font.render("STOCKAGE", True, VERT_BORD)
        fenetre.blit(titre_i, (self.rect_inv.x + 20, self.rect_inv.y + 10))

        # 3. Dessin du Cristal (si le joueur l'a ramassé)
        if joueur.cristal:
            if image_cristal:
                # Si tu as une image dans ton dict ASSETS, on l'utilise et on la redimensionne
                img = pygame.transform.scale(image_cristal, (120, 120))
                fenetre.blit(img, self.rect_cristal.topleft)
            else:
                # Sinon, on dessine un losange phosphorescent basique par défaut
                points = [(self.rect_cristal.centerx, self.rect_cristal.top),
                          (self.rect_cristal.right, self.rect_cristal.centery),
                          (self.rect_cristal.centerx, self.rect_cristal.bottom),
                          (self.rect_cristal.left, self.rect_cristal.centery)]
                coul = VERT_PHOSPHORE if self.en_place else (100, 200, 255)
                pygame.draw.polygon(fenetre, coul, points)
                pygame.draw.polygon(fenetre, BLANC, points, 2)

        # 4. Textes d'indications dynamiques
        if self.resolu:
            txt = self.font.render("SYSTEME ALIMENTE. PROTOCOLE DE DECOLLAGE INITIE.", True, VERT_PHOSPHORE)
        elif not joueur.cristal:
            txt = self.font.render("ERREUR : CRISTAL D'ALIMENTATION MANQUANT.", True, ROUGE_ALERTE)
        elif not self.en_place:
            txt = self.font.render("INSEREZ LE CRISTAL DANS LE REACTEUR.", True, ORANGE_TACTIQUE)
        elif not getattr(joueur, "a_tango", False):
             txt = self.font.render("CRISTAL ALIMENTE. ATTENTE DU PERSONNEL (TANGO).", True, ORANGE_TACTIQUE)
        
        fenetre.blit(txt, txt.get_rect(center=(self.L//2, self.H - 100)))
        
        # Indication pour quitter
        aide = self.font.render("Appuyez sur ECHAP pour fermer le panneau", True, VERT_BORD)
        fenetre.blit(aide, aide.get_rect(center=(self.L//2, self.H - 50)))