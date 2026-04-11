import pygame
import webbrowser
import assets
import jeu
import option
import dl
import rejoindre
import sauvegarde

pygame.init()

#Fénétre jeu
fenetre = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
WIDTH, HEIGHT = fenetre.get_size()

#Titre et logo de la fenêtre
pygame.display.set_caption("D-RED")
pygame.display.set_icon(pygame.image.load("ressource/logo.png"))

#Musique de fond
pygame.mixer.music.load(assets.ASSETS['musique_menu'])
pygame.mixer.music.play(-1) #Musique en boucle

#image de fond
backgroundori = pygame.image.load("ressource/images.png").convert()
background = pygame.transform.scale(backgroundori, (WIDTH, HEIGHT)) 
imgsite = pygame.image.load("ressource/site.png").convert_alpha()
img_site = pygame.transform.scale(imgsite, (WIDTH*0.03, HEIGHT*0.05))
rect_site = img_site.get_rect()

#Couleur
WHITE = (255,255,255)
SHADOW = (0,0,0,150)
BLACK = (0,0,0)
GLASS_BORDER = (255, 255, 255, 150)
GOLD = (255, 215, 0)
GOLD_BRILLANT = (218, 179, 10)
GOLD_TRANSPARENT = (255, 215, 0, 100)

#Police
FONT_TITLE = pygame.font.Font("ressource/PoliceFarland2.ttf", 80)
FONT_BUTTON = pygame.font.Font("ressource/police.ttf", 28)

class Button:
    def __init__(self,text, action):
        self.text = text
        self.action = action
        self.width = 0
        self.height = 0
        self.rect = pygame.Rect((0,0,0,0))
        self.led = 0
        self.dore = 0
        self.txtsurf = None
        self.shadow = None
        self.txtrect = None
    
    def update_pos(self, x, y, L, H): #met a jour les boutons si on change de res
        self.width = L
        self.height = H
        self.rect = pygame.Rect(x, y, L, H)
        self.txtsurf = FONT_BUTTON.render(self.text, True, WHITE)
        self.shadow = FONT_BUTTON.render(self.text, True, SHADOW)
        self.txtrect = self.txtsurf.get_rect(center=(L//2, H//2))
    
    def draw(self, win, mouse_pos):
        is_hover = self.rect.collidepoint(mouse_pos) #Sur rectangle ou pas ?
        #Effet lumineux
        if is_hover:
            self.led = min(255,self.led + 15)
            self.dore = min(255,self.dore + 20)
        else:
            self.led = max(0,self.led - 15)
            self.dore = max(0,self.dore - 20)

        # Effet doré lors du survol
        if is_hover:
            gold_rect = self.rect.inflate(10, 10) #Rectangle contour
            pygame.draw.rect(win, GOLD_BRILLANT, gold_rect, width=3, border_radius=20)

        # Dessiner le bouton avec effet de verre
        if is_hover:
            color = GOLD_TRANSPARENT
        else:
            color = GLASS_BORDER
        #Transparence
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, color, (0, 0, self.width, self.height), border_radius=15)
        pygame.draw.rect(button_surface, GLASS_BORDER, (0, 0, self.width, self.height), width=1, border_radius=15)

        # Effet de lueur
        if self.led > 0:
            pygame.draw.rect(button_surface, (*GOLD, self.led), (20, self.height - 6, self.width - 40, 4), border_radius=15)
        
        button_surface.blit(self.shadow, (self.txtrect.x + 1, self.txtrect.y + 1))
        button_surface.blit(self.txtsurf, self.txtrect)
        win.blit(button_surface, self.rect)

#Recalcul de la resolution après le menu des options
def update_resolution(L, H):
    #Pour modif variable global
    global background, FONT_TITLE, FONT_BUTTON, WIDTH, HEIGHT, rect_site
    global title1, shadow1, title2, shadow2, x1, y1, x2, y2
    WIDTH,HEIGHT = L,H
    #Redimensionner l'image de fond
    background = pygame.transform.scale(backgroundori, (L, H))
    #Taille police par nouvelle resolution
    tailletitre = int(80*H/1080)
    taillebutoon=int(28*H/1080)
    FONT_TITLE = pygame.font.Font("ressource/PoliceFarland2.ttf", tailletitre)
    FONT_BUTTON = pygame.font.Font("ressource/police.ttf", taillebutoon)
    #Redimensionner l'image du site
    rect_site = img_site.get_rect(bottomright=(L-30, H-30))
    #Titre et ombre
    title1 = FONT_TITLE.render("FarLand", True, WHITE)
    shadow1= FONT_TITLE.render("FarLand", True, SHADOW)
    title2=FONT_TITLE.render("Venture", True, WHITE)
    shadow2=FONT_TITLE.render("Venture", True, SHADOW)
    #Pos des titre
    x1 = (int(L*0.75)) - (title1.get_width()//2)
    y1= (int(H*0.20))
    y2 = y1+ title1.get_height() - 10
    x2 = (int(L*0.75)) - (title2.get_width()//2)

    #Repositionner les boutons
    btnespace = (int(H*0.02))
    #Largeur et hauteur des boutons en fonction de la résolution
    btnL=(int(L*0.19))
    btnH=(int(H*0.05))
    startX = (int(L*0.75))-(btnL//2)
    startY= (int(H*0.38))
    #Met à jour la position des boutons
    for i, button in enumerate(buttons):
        posy = startY+i*(btnH+btnespace)
        button.update_pos(startX, posy, btnL, btnH)

def retourmenu():
    #Recharge menu apres partie
    pygame.event.clear()
    #Remet res
    nouvres = pygame.display.get_surface()
    nouvlard, nouvhaut = nouvres.get_size()
    update_resolution(nouvlard, nouvhaut)
    #Remet musique
    pygame.mixer.music.load(assets.ASSETS['musique_menu'])
    pygame.mixer.music.play(-1)

#Les boutons
buttons = [
    Button("Nouvelle Partie","new"),
    Button("Charger Partie", "load"),
    Button("Heberger Partie", "hote"),
    Button("Rejoindre Partie", "rejoindre"),
    Button("Options", "options"),
    Button("Quitter", "quit")
]

#On l'appelle une première fois pour initialiser les positions
update_resolution(WIDTH, HEIGHT)

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # Limite à 60 FPS
    clickmouse = False
    #Evenements Souris et fermetue jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clickmouse = True

    #Fond de depart
    fenetre.blit(background, (0,0))

    #Affichage sur ecran les titres
    fenetre.blit(shadow1, (x1 + 3, y1 + 3))
    fenetre.blit(title1, (x1, y1))
    fenetre.blit(shadow2, (x2 + 3, y2 + 3))
    fenetre.blit(title2, (x2, y2))
    fenetre.blit(img_site, rect_site)
    #Coordonne souris et action
    mouse_pos = pygame.mouse.get_pos()
    #Ouvrir le site web en cliquant sur l'image du site
    if clickmouse and rect_site.collidepoint(mouse_pos):
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    #Logique et affichage boutons
    for button in buttons:
        button.draw(fenetre, mouse_pos)
        if clickmouse and button.rect.collidepoint(mouse_pos):
            #Nouvelle partie
            if button.action == "new":
                pygame.mixer.music.fadeout(500) #Baisse en fondu le son
                #lance le Chagement
                dl.ecran_chargement(fenetre, WIDTH, HEIGHT)
                #lance le Mode Hote
                jeu.lancer(fenetre, mode = "solo")
                retourmenu()
            #Mode host
            elif button.action == "hote":
                pygame.mixer.music.fadeout(500)
                #Chargement
                dl.ecran_chargement(fenetre, WIDTH, HEIGHT)
                #Mode Hote
                jeu.lancer(fenetre, mode = "hote")
                retourmenu()
            #Charger Partie
            elif button.action == "load":
                save = sauvegarde.charger()
                if save:
                    pygame.mixer.music.fadeout(500)
                    dl.ecran_chargement(fenetre, WIDTH, HEIGHT)
                    jeu.lancer(fenetre, mode="solo", save=save)
                    retourmenu()
            #Options
            elif button.action == "options":
                # Lancer le menu des options
                fenetre=option.option_menu(fenetre, WIDTH, HEIGHT)
                retourmenu()
            #Rejoindre
            elif button.action == "rejoindre":
                ip = rejoindre.rejoindre(fenetre, WIDTH,HEIGHT) #OUvre ecran pour rentrer IP
                if ip: #Si l'IP est rentré
                    pygame.mixer.music.fadeout(500)
                    #Chargement
                    dl.ecran_chargement(fenetre, WIDTH, HEIGHT)
                    #Mode Client
                    jeu.lancer(fenetre, mode = "client", ip=ip)
                    retourmenu()
            #Quitter le jeu
            elif button.action == "quit":
                running = False
    #Met ajour affichage
    pygame.display.flip()
pygame.quit()