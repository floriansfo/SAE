import pygame
import random

VERTFOND = (10,25,15,210)
VERTBORD = (45,90,55)
VERTPHOSPHORE = (100,255,150)
VERTECLAT = (180,255,200)
BLANC = (240,255,240)
ROUGE = (255,60,60)
ORANGE =(255,170,50)
BLEU = (100,180,255)
#Cache pour opti
CACHE = {}
surfalpha = None
policemode = None
policeoxy = None

def textee(police, texte, couleur):
    cle = (texte, couleur)
    if cle not in CACHE:
        CACHE[cle] = police.render(texte, True, couleur)
    return CACHE[cle]

def panneau(fenetre,x,y,w,h):
    global surfalpha
    if surfalpha is None or surfalpha.get_size() != fenetre.get_size():
        surfalpha = pygame.Surface(fenetre.get_size(), pygame.SRCALPHA)
    surfalpha.fill((0,0,0,0), (x,y,w,h))
    #Fond
    pygame.draw.rect(surfalpha, VERTFOND, (x,y,w,h), border_radius=4)
    fenetre.blit(surfalpha, (x,y), (x,y,w,h))
    #Bordure
    pygame.draw.rect(fenetre, VERTBORD, (x,y,w,h), 2, border_radius=4)
    #Coin eclairé
    pygame.draw.line(fenetre, VERTPHOSPHORE, (x,y+6), (x, y+16), 3)
    pygame.draw.line(fenetre, VERTPHOSPHORE, (x+6,y), (x+16, y), 3)

def overlay_HUD():
    police = pygame.font.Font("ressource/police.ttf",24)
    hudmode = pygame.image.load("ressource/HUD_mc_V2.png").convert_alpha()
    hudinventaire = pygame.image.load("ressource/HUD_inventaire.png").convert_alpha()
    coeur = pygame.image.load("ressource/coeur_hp.png").convert_alpha()
    coeur = pygame.transform.scale(coeur, (30,30))
    inventaire = False
    return police, hudmode, hudinventaire, inventaire, coeur

def onventaire(fenetre, inventaire, hudinventaire, LARGEUR, HAUTEUR):
    if inventaire:
        dessus = hudinventaire.get_rect(center = (LARGEUR//2, HAUTEUR//2))
        fenetre.blit(hudinventaire, dessus)

def mode_texte(fenetre, m_combat, enpause, police, hudmode, inventaire):
    global policemode
    if policemode is None:
        policemode = pygame.font.Font("ressource/police.ttf",48)
    fenetre.blit(hudmode, (10,10))
    if enpause:
        texte = "PAUSE"
    elif inventaire:
        texte = "INVENTAIRE"
    elif m_combat == True:
        texte = "COMBAT"
    else:
        texte = "EXPLORATION"
    surface = textee(policemode, texte, BLANC)
    surfacerect = surface.get_rect()
    surfacerect.center = (10+hudmode.get_width()//2, 10+hudmode.get_height()//2)
    fenetre.blit(surface, surfacerect)

def pieces(fenetre, joueur, police, LARGEUR):
    texte = textee(police, f"PIECES: {joueur.pieces}", ORANGE)
    w,h = texte.get_width()+30,40
    x,y = LARGEUR-w-10,65
    panneau(fenetre, x, y, w, h)
    fenetre.blit(texte, texte.get_rect(center=(x+w//2, y+h//2)))

def horloge(fenetre, police, jour, heure, LARGEUR):
    DUREE = 28800
    heure = min(heure, DUREE)
    heurejeu = 6+(heure/DUREE)*14
    heures, minutes = int(heurejeu), int((heurejeu-int(heurejeu))*60)
    restant = DUREE-heure
    if restant>7200:
        couleur = VERTPHOSPHORE
    elif restant>2880:
        couleur = ORANGE
    else:
        couleur = ROUGE
    texte = textee(police, f"JOUR {jour} | {heures:02d}:{minutes:02d}", couleur)
    w,h = texte.get_width()+30,45
    x,y = LARGEUR-w-10,10
    panneau(fenetre, x, y, w, h)
    fenetre.blit(texte, texte.get_rect(center=(x+w//2, y+h//2)))
    if heurejeu >= 18 and pygame.time.get_ticks()%1000<500:
        alerte = textee(police, "ALERTE: RENTRER AU VAISSEAU", ROUGE)
        fenetre.blit(alerte, alerte.get_rect(center=(LARGEUR//2, 80)))

def arme_overlay(fenetre, joueur, image, HAUTEUR, present):
    posx = 415+(present//4)
    posy = HAUTEUR-66
    imgarme = image.get(joueur.arsenal)
    imgarme = pygame.transform.scale(imgarme, (160,50))
    fenetre.blit(imgarme, (posx, posy))

def munition(fenetre, joueur, police, img, HAUTEUR):
    panneau(fenetre, 320, HAUTEUR-71, 260, 60)
    couleur = VERTPHOSPHORE if joueur.munition > 0 else ROUGE
    texte = textee(police, f"x{joueur.munition}", couleur)
    posx = 330
    posy = HAUTEUR-56
    imgvert = img.copy()
    imgvert.fill(VERTPHOSPHORE, special_flags=pygame.BLEND_RGBA_MULT)
    imgvert = pygame.transform.scale(imgvert, (50,50))
    fenetre.blit(imgvert, (posx-8, posy-10))
    fenetre.blit(texte, (posx+40, posy+3))

def endurance(fenetre, joueur, course, HAUTEUR, LARGEUR):
    largeur, hauteur = 240,10
    x,y = LARGEUR//2-largeur//2, HAUTEUR-30
    fin = joueur.endurance/joueur.maxcourse
    couleur = VERTECLAT if fin >0.25 else ROUGE
    pygame.draw.rect(fenetre, (20,30,20), (x, y, largeur, hauteur), border_radius=3)
    if fin >0:
        pygame.draw.rect(fenetre, couleur, (x, y, int(fin*largeur), hauteur), border_radius=3)
    pygame.draw.rect(fenetre, VERTBORD, (x, y, largeur, hauteur), 1, border_radius=3)
    #Etincelle quand course
    if course and fin >0 :
        for _ in range(5):
            px, py = random.randint(-5,5), random.randint(-2, hauteur+2)
            pygame.draw.circle(fenetre, VERTECLAT, (int(x+(fin*largeur)+px), int(y+py)),1)

def lampe(fenetre, joueur, police, img_lampe, HAUTEUR):
    panneau(fenetre, 15, HAUTEUR-131,290,120)
    x,y = 30,HAUTEUR-115
    if not joueur.possedelampe:
        texte = textee(police, "LUM: --", ROUGE)
        fenetre.blit(texte, (x,y))
        return
    p = int((joueur.pile/joueur.pilemax)*100)
    if p >50:
        couleur = VERTPHOSPHORE
    elif p > 20:
        couleur = ORANGE
    else:
        couleur = ROUGE
    imglampe = img_lampe.copy()
    imglampe.fill(couleur, special_flags=pygame.BLEND_RGB_ADD)
    imglampe = pygame.transform.scale(imglampe, (40,40))
    fenetre.blit(imglampe, (x,y-10))
    etat = "ON" if joueur.lumiereallumee else "OFF"
    texte = textee(police, f"{p}% {etat}", couleur)
    fenetre.blit(texte, (x+40,y))
    pygame.draw.rect(fenetre, (30,40,30), (x+140,y+8,100,6), border_radius=2)
    if p>0:
        pygame.draw.rect(fenetre, couleur, (x+140,y+8,int((p/100)*100),6), border_radius=2)

def oxygene(fenetre, joueur, police, LARGEUR, HAUTEUR):
    global policeoxy
    if policeoxy is None:
        policeoxy = pygame.font.Font("ressource/titre.ttf",24)
    largeur, hauteur = 200,10
    x,y = 70, HAUTEUR-75
    oxy = max(0, joueur.oxygene/joueur.oxygenemax)
    texteoxy = textee(policeoxy, "O²", BLEU)
    fenetre.blit(texteoxy, (x-40,y-6))
    if oxy>0.3:
        couleur = BLEU
    elif oxy>0.1:
        couleur = ORANGE
    else:
        couleur = ROUGE
    pygame.draw.rect(fenetre, (20,30,20), (x, y, largeur, hauteur), border_radius=3)
    largeurbarre = int(oxy*largeur)
    if largeurbarre>0:
        pygame.draw.rect(fenetre, couleur, (x, y, largeurbarre, hauteur), border_radius=3)
    pygame.draw.rect(fenetre,(60,100,140), (x, y, largeur, hauteur),1, border_radius=3)
    if oxy <= 0 and pygame.time.get_ticks()%800<400:
        alerte = textee(police, "ASPHYXIE", ROUGE)
        fenetre.blit(alerte, alerte.get_rect(center=(160,HAUTEUR-170)))

def hud_life(fenetre, LARGEUR, HAUTEUR, hp_cur, hp_max, police, coeur):
    x,y = 20, HAUTEUR-45
    rectnb = 20
    rectL, rectH = 8,18
    rectpos = int((hp_cur/hp_max)*rectnb)
    fenetre.blit(coeur, (x,y-4))
    for i in range(rectnb):
        rectposx = x+30+(i*(rectL+2))
        couleur = VERTPHOSPHORE if i < rectpos else (40,55,45)
        pygame.draw.rect(fenetre, couleur, (rectposx, y, rectL, rectH))
    textehp = textee(police, f"{int(hp_cur)}", VERTECLAT)
    fenetre.blit(textehp, (x+45+(rectnb*10), y-4))