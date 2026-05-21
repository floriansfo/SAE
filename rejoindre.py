import pygame
import sys

#Couleur
WHITE = (255,255,255)
BLACK = (0,0,0)
GOLD = (255,215,0)

#Class bouton
class Button:
    def __init__(self, text, x, y, w, h, action=None):
        self.rect = pygame.Rect(x, y, w, h) #Rectangle du bouton
        self.text = text #Texte du bouton
        self.hover = False #Survol du bouton

    def draw(self, surface, font):
        #Couleur du bouton au survol
        if self.hover:
            dessus = GOLD 
        else:
            dessus = BLACK
        #Transparence
        fond = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(fond,(0,0,0,150),(0,0,self.rect.width,self.rect.height), border_radius=10)
        surface.blit(fond, self.rect.topleft)
        #Bordure du bouton
        pygame.draw.rect(surface, dessus, self.rect,2, border_radius=10)
        #Texte du bouton
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos,clique):
        #Verirife si cliqué et survolé
        self.hover = self.rect.collidepoint(pos)
        return self.hover and clique

def rejoindre(fenetre, L, H):
    clock = pygame.time.Clock()
    imgori = pygame.image.load("ressource/images/option.png").convert()
    imgfond = pygame.transform.scale(imgori, (L,H))

    #Taille texte et police
    taille_titre = max(30, int(H*0.08))
    taille_texte = max(15, int(H*0.035))
    fontitle = pygame.font.Font("ressource/fonts/titre.ttf", taille_titre)
    fonttexte = pygame.font.Font("ressource/fonts/police.ttf", taille_texte)

    #Parametre barre IP
    ip = "51.38.115.211"
    iprect = pygame.Rect(L//2-250, H//2-25, 500, 50)

    #Bouton
    btnw = max(200, int(L*0.20))
    btnh = max(40, int(H*0.07))
    btn_retour = Button("ANNULER", L//2-btnw-20, H//2+80, btnw, btnh)
    btn_valider = Button("VALIDER", L//2+20, H//2+80, btnw, btnh)
    running = True
    while running:
        pos = pygame.mouse.get_pos()
        clique = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clique = True
            #Gestion ecriture au clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_RETURN:
                    return ip
                elif event.key == pygame.K_BACKSPACE:
                    ip = ip[:-1]
                else:
                    if len(ip)<15 and event.unicode.isprintable():
                        ip = ip + event.unicode
            #Si redimensionne la fenetre
            if event.type == pygame.VIDEORESIZE:
                L,H = event.w, event.h
                fenetre = pygame.display.set_mode((L,H), pygame.RESIZABLE)
                imgfond = pygame.transform.scale(imgori, (L,H))
                iprect = pygame.Rect(L//2-250, H//2-25, 500, 50)
                btnw = max(200, int(L*0.20))
                btnh = max(40, int(H*0.07))
                btn_retour.rect.update(L//2-btnw-20,H//2+80, btnw, btnh)
                btn_valider.rect.update(L//2+20,H//2+80, btnw, btnh)
                #Taile texte
                taille_titre = max(30, int(H*0.08))
                taille_texte = max(15, int(H*0.035))
                fontitle = pygame.font.Font("ressource/fonts/titre.ttf", taille_titre)
                fonttexte = pygame.font.Font("ressource/fonts/police.ttf", taille_texte)
        if btn_retour.is_clicked(pos, clique):
            return None
        if btn_valider.is_clicked(pos, clique):
            return ip
        #Dessine
        fenetre.blit(imgfond,(0,0))
        #Titre
        titre = fontitle.render("REJOINDRE UNE PARTIE", True, WHITE)
        fenetre.blit(titre, (L//2-titre.get_width()//2, int(H*0.15)))
        #Texte
        texte = fonttexte.render("ENTREZ IP DU SERVEUR:", True, GOLD)
        fenetre.blit(texte, (L//2-texte.get_width()//2, H//2-80))
        #Barre IP
        fondbarre = pygame.Surface((iprect.width, iprect.height), pygame.SRCALPHA)
        pygame.draw.rect(fondbarre, (0,0,0,180),(0,0,iprect.width,iprect.height), border_radius=10)
        fenetre.blit(fondbarre, iprect.topleft)
        pygame.draw.rect(fenetre, GOLD, iprect, 2, border_radius=10)
        #Texte affiche IP
        txt = fonttexte.render(ip, True, WHITE)
        fenetre.blit(txt, (iprect.x+20, iprect.y+iprect.height//2-txt.get_height()//2))
        #Dessine bouton
        btn_retour.draw(fenetre,fonttexte)
        btn_valider.draw(fenetre,fonttexte)
        pygame.display.flip()
        clock.tick(60)
    return None