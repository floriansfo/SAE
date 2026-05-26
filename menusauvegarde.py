import pygame
import sys
import sauvegarde

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
GOLD_TRANSPARENT = (255, 215, 0, 60)
GRIS = (180, 180, 180)








class PanneauSlot :
    def __init__(self, slot, save_data) :
        self.slot =slot# num slot
        self.save = save_data # save data or None
        self.rect = pygame.Rect(0, 0, 0, 0)
        
        
        self.selectionne = False

    def update_pos(self, x, y, w, h): # si changement de res
        self.rect = pygame.Rect(x, y, w, h)






    def draw(self, fenetre, font_titre, font_texte) : # fct pour draw panneau slot avec infos de la save 
        
        
        #background
        fond =pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)\
        
        
        if self.selectionne :
            
            pygame.draw.rect(fond, GOLD_TRANSPARENT, (0, 0, self.rect.width, self.rect.height),border_radius=12)
            pygame.draw.rect(fond, GOLD, (0, 0, self.rect.width, self.rect.height), 2, border_radius=12)
        
        else:
            pygame.draw.rect(fond, (0, 0, 0, 150), (0, 0, self.rect.width, self.rect.height), border_radius=12)
            pygame.draw.rect(fond, WHITE, (0, 0, self.rect.width, self.rect.height), 1, border_radius=12)
            
        
        fenetre.blit(fond, self.rect.topleft)

        #title
        if self.selectionne:
            couleur_titre = GOLD
        else:
            couleur_titre = WHITE
        titre =font_titre.render(f"SLOT {self.slot}", True, couleur_titre)
        
        fenetre.blit(titre, (self.rect.centerx - titre.get_width() // 2, self.rect.y + 15)) 

        #content
        if self.save is None:
            
            vide = font_texte.render("--- VIDE ---", True, GRIS)
            fenetre.blit(vide, (self.rect.centerx - vide.get_width() // 2, self.rect.centery - vide.get_height() // 2))
            
        else:
            
            
            infos = [
                f"Niveau : {self.save.get('niveau_actuel', '?')}",
                f"HP : {self.save['joueur'].get('hp', '?')} / {self.save['joueur'].get('hpmax', '?')}",
                f"Arme : {self.save['joueur'].get('arsenal', '?')}",
                f"Pieces : {self.save['joueur'].get('pieces', '?')}",
                f"Malachite : {self.save['joueur'].get('malachite', '?')}",
                f"Date : {self.save.get('date', '?')}",
            ]
            
            
            
            debut_y = self.rect.y + titre.get_height() + 30
            
            for i, ligne in enumerate(infos): # boucle pour display les infos de la save
                txt = font_texte.render(ligne, True, WHITE)
                
                fenetre.blit(txt, (self.rect.centerx - txt.get_width() // 2, debut_y + i * (txt.get_height() + 10)))




    def is_clicked(self, pos, clique):
        return self.rect.collidepoint(pos) and clique






class Bouton:
    def __init__(self, texte):
        self.texte = texte
        self.rect =pygame.Rect(0, 0, 0, 0)
        self.hover = False

    def update_pos(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)



    def draw(self, fenetre, font) : # fct pour draw les boutons charger/sauvegarder et annuler
        
        
        fond = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        pygame.draw.rect(fond, (0, 0, 0, 150), (0, 0, self.rect.width, self.rect.height), border_radius=10)
        
        fenetre.blit(fond, self.rect.topleft)
        
        
        if self.hover:
            couleur_bord = GOLD
        else:
            couleur_bord = BLACK
            
            
        pygame.draw.rect(fenetre, couleur_bord, self.rect, 2, border_radius=10)
        txt = font.render(self.texte, True, WHITE)
        
        
        fenetre.blit(txt, (self.rect.centerx - txt.get_width() // 2, self.rect.centery - txt.get_height() // 2))


    def is_clicked(self, pos, clique):
        self.hover = self.rect.collidepoint(pos)
        
        return self.hover and clique








def selectionner_sauvegarde(fenetre, L, H, mode="charger"):
    # charger pour load et sauvegarder pour select le slot ou ecrire la sauvegarde
    
    
    clock = pygame.time.Clock() # controle frame
    imgori = pygame.image.load("ressource/images/option.png").convert()
    imgfond = pygame.transform.scale(imgori, (L, H))

    taille_titre =max(30, int(H * 0.08))
    taille_texte = max(15, int(H * 0.03))
    
    
    
    #polices
    font_titre = pygame.font.Font("ressource/fonts/titre.ttf", taille_titre)
    font_slot = pygame.font.Font("ressource/fonts/police.ttf", max(18, int(H * 0.035)))
    font_texte = pygame.font.Font("ressource/fonts/police.ttf", taille_texte)

    #load les données des 3 slots
    saves = sauvegarde.charger_tous()

    #faire les panneaux 
    panneaux = []
    for i in range(3):
        panneaux.append(PanneauSlot(i + 1, saves[i])) # decal pour begin a 1 et pas 0




    if mode == "charger":
        texte_action = "CHARGER PARTIE"
        label_btn = "CHARGER"
    else:
        texte_action = "SAUVEGARDER"
        label_btn = "SAUVEGARDER"

    btn_action = Bouton(label_btn)
    
    
    btn_annuler = Bouton("ANNULER")

    slot_selectionne = None

    def update_positions(newL, newH): # au cas res encore
        
        marge = int(newL * 0.05)
        ecart = int(newL * 0.02)
        
        panneau_w = (newL - 2 * marge - 2 * ecart) // 3
        panneau_h = int(newH * 0.50)
        panneau_y = int(newH * 0.22)
        
        
        for i, panneau in enumerate(panneaux):
            
            x = marge + i * (panneau_w + ecart)
            panneau.update_pos(x, panneau_y, panneau_w, panneau_h)
            
            
        #btns en bas
        btnw = max(180, int(newL * 0.15))
        btnh = max(40, int(newH * 0.06))
        
        btn_y = int(newH * 0.82)
        
        btn_action.update_pos(newL // 2 - btnw - 20, btn_y, btnw, btnh)
        btn_annuler.update_pos(newL // 2 + 20, btn_y, btnw, btnh)

    update_positions(L, H)

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
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            
            if event.type == pygame.VIDEORESIZE:
                L, H = event.w, event.h
                fenetre = pygame.display.set_mode((L, H), pygame.RESIZABLE)
                imgfond = pygame.transform.scale(imgori, (L, H))
                
                update_positions(L, H)

        #gestion clics sur panneaux
        for panneau in panneaux:
            if panneau.is_clicked(pos, clique):
                slot_selectionne = panneau.slot
                for p in panneaux:
                    p.selectionne = (p.slot == slot_selectionne)


        #btns pour les actions
        
        
        if slot_selectionne is not None:
            
            slot_valide = True
        
        else:
            
            slot_valide = False
            
        if mode == "charger":
            
            if slot_selectionne is not None and saves[slot_selectionne - 1] is not None:
                
                slot_valide = True
            else:
                slot_valide = False
                
        if btn_action.is_clicked(pos, clique) and slot_valide:
            
            return (saves[slot_selectionne - 1], slot_selectionne)

        #annuler
        if btn_annuler.is_clicked(pos, clique):
            return None

        #draw le tout
        fenetre.blit(imgfond, (0, 0))
        titre = font_titre.render(texte_action, True, WHITE)
        fenetre.blit(titre, (L // 2 - titre.get_width() // 2, int(H * 0.07)))
        
        
        for panneau in panneaux:
            panneau.draw(fenetre, font_slot, font_texte)
            
            
        btn_action.draw(fenetre, font_texte)
        btn_annuler.draw(fenetre, font_texte)
        pygame.display.flip()
        
        
        
        clock.tick(60)

    return None
