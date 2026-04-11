import pygame
import sys
import assets

pygame.init()
#Fenetre en plein ecran
fenetre = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
#taille ecran actuelle
WIDTH, HEIGHT = fenetre.get_size()
assets.ASSETS=assets.charger_assets(WIDTH, HEIGHT)
pygame.display.set_caption("D-RED")
#Cacher la souris
pygame.mouse.set_visible(False)
#Couleurs
BLACK = (0,0,0)

#Charmenent assets
logoori = assets.ASSETS.get('img_logo')
logo = pygame.transform.scale(logoori, (250,250))
centre_logo = logo.get_rect(center=(WIDTH//2, HEIGHT//2))

def demarrage():
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    duration = 1500 #1.5 Seconde 
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #Calcul temps
        tamps = pygame.time.get_ticks() - start_time
        #Calcul animation en %, min pour pas depasse 1
        arrive = min(tamps/ duration, 1.0)
        #Fond noir
        fenetre.fill(BLACK)
        #Logo fondu
        if logo is not None:
            #arrive deviens une valeur d'opacite entre 0 et 255
            fondu = int(arrive*255)
            logo.set_alpha(fondu) 
            fenetre.blit(logo, centre_logo)
        pygame.display.flip()
        #Quand il est affiché
        if arrive >=1.0:
            pygame.time.delay(1000) #On laisse pendant 2 sec apres l'affichage du logo 
            return
demarrage()
#Remet la souris
pygame.mouse.set_visible(True)
#Lance menu
import menu