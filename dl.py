import pygame
import sys
import time
import assets
logo = assets.ASSETS['img_load']

def ecran_chargement(fenetre, WIDTH, HEIGHT):
    # Couleurs
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    logores = pygame.transform.scale(logo, (WIDTH, HEIGHT))
    r = HEIGHT/1080.0
    tailletxt = int(70*r)
    # Police
    FONT_TITLE = pygame.font.Font("ressource/fonts/police.ttf", tailletxt)   
    fenetre.fill(BLACK)
    # Afficher le logo
    fenetre.blit(logo, (0, 0))
    # Afficher le texte de chargement
    texte = FONT_TITLE.render("CHARGEMENT...", True, WHITE)
    mx = int(50*(WIDTH/1920))
    my = int(50*(HEIGHT/1080))
    texte_rect = texte.get_rect(bottomright=(WIDTH - mx, HEIGHT - my))
    fenetre.blit(texte, texte_rect)
    # Mettre à jour l'affichage
    pygame.display.flip()
    pygame.event.pump()  # Traiter les événements pour éviter que la fenêtre ne se fige
    return