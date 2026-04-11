import pygame
import math
import assets
from prerequis import ZOOM, LARGEURMAP, HAUTEURMAP, SOL, ASCENCEUR, ETOILE, FLAMME, MUR
from vaisseau import BOUTIQUE, LIT
import monstre

def dessinerjeu(ecran, LARGEUR, HAUTEUR, carte, joueur, objets, piecessol, monstres, joueursup, niveau_actuel, connect, lumieremarche, filtre):
    #Suivi joueur
    camera_x = (LARGEUR//2)-joueur.rect.centerx
    camera_y = (HAUTEUR//2)-joueur.rect.centery

    #Calcul des limites de camera pour optimiser
    minx = max(0, -camera_x//ZOOM-1)
    maxx = min(LARGEURMAP, (-camera_x+LARGEUR)//ZOOM+2)
    miny = max(0, -camera_y//ZOOM-1)
    maxy = min(HAUTEURMAP, (-camera_y+HAUTEUR)//ZOOM+2)

    #Image save
    img_sol=assets.ASSETS['img_sol']
    img_ascenseur=assets.ASSETS['img_ascenseur']
    img_murtop=assets.ASSETS['img_murtop']
    img_murface=assets.ASSETS['img_murface']
    img_ballevol=assets.ASSETS['img_ballevol']
    img_piece=assets.ASSETS['img_piece']
    img_etoile = assets.ASSETS['img_etoile']
    img_flamme = assets.ASSETS['img_flamme']
    img_lit = assets.ASSETS['img_lit']
    img_boutique = assets.ASSETS['img_boutique']
    animationjoueur = assets.ASSETS['animationjoueur']

    #Dessiner le sol
    ecran.fill((0,0,0))
    for y in range(miny, maxy):
        for x in range(minx, maxx):
            case = carte[y][x]
            screen_x = x * ZOOM + camera_x
            screen_y = y * ZOOM + camera_y
            if case == SOL and img_sol is not None:
                ecran.blit(img_sol, (screen_x,screen_y))
            elif case == ASCENCEUR and img_ascenseur is not None:
                ecran.blit(img_ascenseur, (screen_x, screen_y))
            elif case == ETOILE:
                ecran.blit(img_etoile, (screen_x, screen_y))
            elif case == FLAMME:
                ecran.blit(img_flamme, (screen_x,screen_y))
            elif case == LIT:
                ecran.blit(img_lit, (screen_x,screen_y))
            elif case == BOUTIQUE:
                ecran.blit(img_boutique, (screen_x, screen_y))
    
    #Liste de chosses a dessiner apres le sol
    adessiner = []

    #Dessin murs
    for y in range(miny, maxy):
        for x in range(minx, maxx):
            case = carte[y][x]
            if case == MUR:
                screen_x = x * ZOOM + camera_x
                screen_y = y * ZOOM + camera_y
                img_mur = img_murtop
                #On regarsde si il y a du sol en dessous
                if y+1<HAUTEURMAP and (carte[y+1][x]==SOL or carte[y+1][x] == ASCENCEUR):
                    img_mur = img_murface
                if img_mur:
                    adessiner.append((screen_y + ZOOM, img_mur,(screen_x,screen_y)))

    #Dessin objets
    for obj in objets:
        fenetre_x = obj.rect.x + camera_x
        fenetre_y = obj.rect.y + camera_y
        if -ZOOM<fenetre_x<LARGEUR and -ZOOM<fenetre_y<HAUTEUR:
            adessiner.append((fenetre_y + obj.rect.height, obj.texture, (fenetre_x, fenetre_y)))
    
    #Dessin monstres
    for m in monstres:
        if not m.mort:
            fenetre_x = m.rect.x + camera_x
            fenetre_y = m.rect.y + camera_y
            if -ZOOM<fenetre_x<LARGEUR and -ZOOM<fenetre_y<HAUTEUR:
                adessiner.append((fenetre_y + m.rect.height, m.texture, (fenetre_x, fenetre_y)))
    
    img_joueur = animationjoueur[joueur.animation]
    joueurtourne = pygame.transform.rotate(img_joueur, joueur.angle)
    rectaffiche = joueurtourne.get_rect(center = (joueur.rect.centerx + camera_x, joueur.rect.centery + camera_y))
    adessiner.append((rectaffiche.bottom, joueurtourne, rectaffiche.topleft))

    #Dessin balle
    for tir in joueur.tir:
        ix = tir.rect.x + camera_x
        iy = tir.rect.y + camera_y
        if -ZOOM<ix<LARGEUR and -ZOOM<iy<HAUTEUR:
            angleballe = math.atan2(tir.dy, tir.dx)
            angle = -math.degrees(angleballe)
            balleangle = pygame.transform.rotate(img_ballevol, angle)
            rectballe = balleangle.get_rect(center=(ix,iy))
            adessiner.append((rectballe.bottom, balleangle, rectballe.topleft))
    
    #Dessin autre joueur
    if connect:
        for idjoueur, autre in joueursup.items():
            if getattr(autre, "etage", 1) == niveau_actuel:
                #Dessine ses balles
                if hasattr(autre, "monstres_reseau"):
                    for mx,my,mmort in autre.monstres_reseau:
                        if not mmort:
                            ix = mx + camera_x
                            iy = my + camera_y
                            if -ZOOM<ix<LARGEUR and -ZOOM<iy<HAUTEUR:
                                pos_y = iy + 200
                                adessiner.append((pos_y, monstre.larry, (ix,iy)))
                #Dessine ses balles
                if hasattr(autre, "balles_reseau"):
                    for ballex, balley, balledx, balledy in autre.balles_reseau:
                        ix = ballex+camera_x
                        iy = balley + camera_y
                        if -ZOOM<ix<LARGEUR and -ZOOM<iy<HAUTEUR:
                            #On crée la balle
                            anglevol = math.atan2(balledy,balledx)
                            angle = -math.degrees(anglevol)
                            balleangle = pygame.transform.rotate(img_ballevol, angle)
                            rectballe = balleangle.get_rect(center=(ix,iy))
                            adessiner.append((rectballe.bottom, balleangle, rectballe.topleft))
                #Dessine son perso
                xjoueur2 = autre.rect.centerx + camera_x
                yjoueur2 = autre.rect.centery + camera_y
                #On dessine que si il est visible
                if -100<xjoueur2<LARGEUR and -100<yjoueur2<HAUTEUR:
                    if not getattr(autre, "mort", False):
                        #Joueur vivant
                        img_autrejoueur = animationjoueur[autre.animation]
                        img_autrejoueur = pygame.transform.rotate(img_autrejoueur, autre.angle)
                    else:
                        img_autrejoueur = animationjoueur[0].copy()
                        img_autrejoueur = pygame.transform.rotate(img_autrejoueur, 90)
                        img_autrejoueur.set_alpha(20)
                    rect_aff = img_autrejoueur.get_rect(center=(xjoueur2, yjoueur2))
                    adessiner.append((rect_aff.bottom, img_autrejoueur, rect_aff.topleft))
    
    #Tri la liste a dessiner par ordre Y
    adessiner.sort(key=lambda x: x[0])
    for i in adessiner:
        ecran.blit(i[1], i[2]) #image, position
    
    #Dessin piece au sol
    for p in piecessol:
        px = p["rect"].x + camera_x
        py = p["rect"].y + camera_y
        if -50<px<LARGEUR and -50<py<HAUTEUR:
            ecran.blit(img_piece, (px, py))

    #Effet Lumiere quand activé
    if niveau_actuel != 0:
        lumieremarche.appliquer(ecran, joueur, filtre.m_combat)