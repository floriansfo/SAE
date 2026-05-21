import pygame
import sys
import time
import assets
logo = assets.ASSETS['img_load']

def ecran_chargement(fenetre, WIDTH, HEIGHT):
    # Couleurs
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    # Police
    FONT_TITLE = pygame.font.Font("ressource/fonts/police.ttf", 70)   
    fenetre.fill(BLACK)
    # Afficher le logo
    fenetre.blit(logo, (0, 0))
    # Afficher le texte de chargement
    texte = FONT_TITLE.render("CHARGEMENT...", True, WHITE)
    texte_rect = texte.get_rect(bottomright=(WIDTH - 50, HEIGHT - 50))
    fenetre.blit(texte, texte_rect)
    # Mettre à jour l'affichage
    pygame.display.flip()
    pygame.event.pump()  # Traiter les événements pour éviter que la fenêtre ne se fige
    return