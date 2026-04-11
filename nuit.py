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

    def update(self, L, H):
        self.L = L
        self.H = H
        self.ombre = pygame.Surface((self.L, self.H)).convert()
        self.ombre.fill((0,0,0))
    
    def nuit(self, ecran, joueur, jour):
        clock = pygame.time.Clock()
        nouveaujour = jour +1
        soin = int(joueur.hpmax*0.30)
        soinpris = min(soin, joueur.hpmax-joueur.hp)
        #Ecran de nuit
        ecrannuit = pygame.Surface((self.L, self.H))
        ecrannuit.fill((0,0,0))
        y = self.H//2-90
        titre = self.fonttitre.render(f"NUIT du {jour} au {nouveaujour}", True, TEXTE)
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
        sointxt = self.fonttexte.render(f"Recupartion de {soinpris} HP", True, VERT)
        ecrannuit.blit(sointxt, sointxt.get_rect(center = (self.L//2,y)))
        #Fondu nuit
        for i in range(0,256,5):
            self.ombre.set_alpha(i)
            ecran.blit(self.ombre,(0,0))
            pygame.display.flip()
            clock.tick(60)
        ecran.blit(ecrannuit,(0,0))
        pygame.display.flip()
        pygame.time.delay(2000)
        joueur.oxygene = joueur.oxygenemax
        joueur.hp += soinpris
        return nouveaujour