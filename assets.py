import pygame
from prerequis import texture, ZOOM
import os

def charger_assets(largeur, hauteur):
    assets = {}
    Z = ZOOM+1
    #Charger les textures
    #sol
    assets['img_sol'] = texture("sol.png",(Z,Z))
    assets['img_sol_rouge']= texture("sol/sol_rouge.png", (Z,Z))
    assets['img_ascenseur'] = texture("ascenseur.png",(Z,Z))
    assets['img_murface'] = texture("murface.png", (Z, Z))
    assets['img_murtop'] = texture("murtop.png", (Z, Z))
    #rouge
    assets['img_murtop_rouge'] = texture("sol/murtop_rouge.png", (Z, Z))
    assets['img_murface_rouge'] = texture("sol/murface_rouge.png", (Z, Z))
    assets['img_lit'] = texture("lit.png", (Z, Z))
    assets['img_boutique'] = texture("shop.png", (Z, Z))
    assets['img_logo'] = texture("logov2.png", (Z, Z))
    assets['img_caisse'] = texture("caisse_loot.png", (Z, Z))
    assets['img_plante'] = texture("plante.png", (Z, Z))
    assets['img_meuble'] = texture("meuble.png", (Z, Z))
    assets['img_lampe'] = texture("lampe.png", (Z, Z))

    assets['img_load'] = texture("Chargement.png", (largeur, hauteur))
    assets['img_piece'] = texture("piece.png", (40,40), transparente=True)
    assets['img_larry'] = texture("Larryv2.png", (200,200), transparente=True)
    assets['img_munition'] = texture("munitionoverlay.png", (80,80), transparente=True)
    assets['img_ballevol'] = texture("balle.png", (45,45), transparente=True)

    assets['mode_combat'] = texture("HUD_mc_V2.png", None, transparente=True)
    assets['mode_inventaire'] = texture("HUD_inventaire.png", None, transparente=True)
    assets['coeur_hp'] = texture("coeur_hp.png", (30,30), transparente=True)
    assets['moteur'] = texture("moteur.png", (ZOOM*3,ZOOM*2), transparente=True)
    assets['img_cassette']= texture("cassette.png", (ZOOM//2,ZOOM//2), transparente=True)
    assets['img_racine'] = texture("racine.png", (Z,Z), transparente=True)


    #decoration pour la map
    assets['img_deco']= {
        'bones':texture("decoration/Bones_shadow1_7.png",(Z,Z), transparente=True),
        'rock1':texture("decoration/Rock1_shadow1_5.png",(Z,Z), transparente=True),
        'rock2':texture("decoration/Rock2_shadow2_1.png",(Z,Z), transparente=True),
        'plant1':texture("decoration/Spike_plant_shadow1_2.png",(Z,Z), transparente=True),
        'plant2':texture("decoration/Spike_plant_shadow1_3.png",(Z,Z), transparente=True),
        'Veins1':texture("decoration/Veins_shadow1_2.png",(Z,Z), transparente=True),
        'Veins2':texture("decoration/Veins_shadow1_3.png",(Z,Z), transparente=True),
        'Veins3':texture("decoration/Veins_shadow1_4.png",(Z,Z), transparente=True),
    }
    assets['img_arme'] = {
        0: texture("couteau.png",(250,80), transparente= True),
        1: texture("pistolet.png",(250,80), transparente= True),
        2: texture("pompe.png",(250,80), transparente= True),
        3: texture("fusil.png",(250,80), transparente= True)
    }

    assets['img_couteau'] = texture("couteauinv.png",(80,80), transparente= True)
    assets['img_pistolet'] = texture("pistoletinv.png",(80,80), transparente= True)
    assets['img_pompe'] = texture("pompeinv.png",(80,80), transparente= True)
    assets['img_fusil'] = texture("fusilinv.png",(80,80), transparente= True)
    assets['img_cristal'] = texture("cristal.png",(80,80), transparente= True)
    assets['img_cristal1'] = texture("cristal1.png",(80,80), transparente= True)
    assets['img_seringue'] = texture("seringue.png",(80,80), transparente= True)

    assets['animationjoueur'] = [
    texture("joueur.png",(100,100), transparente=True),
    texture("joueurgauche.png",(100,100), transparente=True),
    texture("joueurdroit.png",(100,100), transparente=True)
    ]
    #slime assets
    assets['slime_face']=[]
    for i in range(8):
        frame= texture(f"slime/face-{i}.png", (167,167), transparente=True)
        assets['slime_face'].append(frame)
    
    assets['slime_back']=[]
    for i in range(8):
        frame= texture(f"slime/back-{i}.png", (167,167), transparente=True)
        assets['slime_back'].append(frame)
    
    assets['slime_droite']=[]
    for i in range(8):
        frame= texture(f"slime/droite-{i}.png", (167,167), transparente=True)
        assets['slime_droite'].append(frame)

    assets['slime_gauche']=[]
    for i in range(8):
        frame= texture(f"slime/gauche-{i}.png", (167,167), transparente=True)
        assets['slime_gauche'].append(frame)
    #couleur
    assets['couleurs_slime']=[(0,0,0, 80),(100,0,0, 80), (0,100,0,80), (100,50,0,80), (50,100,0,80)]   
    #mort du slime
    assets['slime_mort_face']=[]
    for i in range(9):
        frame= texture(f"slime/mort_face-{i}.png", (167,167), transparente=True)
        assets['slime_mort_face'].append(frame)
    
    assets['slime_mort_back']=[]
    for i in range(9):
        frame= texture(f"slime/mort_back-{i}.png", (167,167), transparente=True)
        assets['slime_mort_back'].append(frame)
    
    assets['slime_mort_droite']=[]
    for i in range(9):
        frame= texture(f"slime/mort_droite-{i}.png", (167,167), transparente=True)
        assets['slime_mort_droite'].append(frame)

    assets['slime_mort_gauche']=[]
    for i in range(9):
        frame= texture(f"slime/mort_gauche-{i}.png", (167,167), transparente=True)
        assets['slime_mort_gauche'].append(frame)
    
    
    #asset nyctobat
    #différentes directions
    assets['nyctobat_face']=[]
    for i in range(1,4):
        frame= texture(f"nyctobat/face-{i}.png", (96,96), transparente=True)
        assets['nyctobat_face'].append(frame)
    
    assets['nyctobat_back']=[]
    for i in range(1,4):
        frame= texture(f"nyctobat/back-{i}.png", (96,96), transparente=True)
        assets['nyctobat_back'].append(frame)
    
    assets['nyctobat_droite']=[]
    for i in range(1,4):
        frame= texture(f"nyctobat/droite-{i}.png", (96,96), transparente=True)
        assets['nyctobat_droite'].append(frame)

    assets['nyctobat_gauche']=[]
    for i in range(1,4):
        frame= texture(f"nyctobat/gauche-{i}.png", (96,96), transparente=True)
        assets['nyctobat_gauche'].append(frame)
    
    #frame de mort: 1 pour chaque pos
    assets['nyctobat_face_dead']=texture(f"nyctobat/face_dead.png",(96,96), transparente=True)
    assets['nyctobat_back_dead']=texture(f"nyctobat/back_dead.png",(96,96), transparente=True)
    assets['nyctobat_droite_dead']=texture(f"nyctobat/droite_dead.png",(96,96), transparente=True)
    assets['nyctobat_gauche_dead']=texture(f"nyctobat/gauche_dead.png",(96,96), transparente=True)

    #asset errant
    assets['errant_face']=[]
    for i in range(1,4):
        frame= texture(f"errant/face-{i}.png", (128,128), transparente=True)
        assets['errant_face'].append(frame)
    
    assets['errant_back']=[]
    for i in range(1,4):
        frame= texture(f"errant/back-{i}.png", (128, 128), transparente=True)
        assets['errant_back'].append(frame)
    
    assets['errant_droite']=[]
    for i in range(1,4):
        frame= texture(f"errant/droite-{i}.png", (128, 128), transparente=True)
        assets['errant_droite'].append(frame)

    assets['errant_gauche']=[]
    for i in range(1,4):
        frame= texture(f"errant/gauche-{i}.png", (128, 128), transparente=True)
        assets['errant_gauche'].append(frame)
    

    #asset xeno
    assets['xeno_face']=[]
    for i in range(10):
        frame= texture(f"xeno/face-{i}.png", (128,128), transparente=True)
        assets['xeno_face'].append(frame)
    
    assets['xeno_back']=[]
    for i in range(10):
        frame= texture(f"xeno/back-{i}.png", (128, 128), transparente=True)
        assets['xeno_back'].append(frame)
    
    assets['xeno_droite']=[]
    for i in range(10):
        frame= texture(f"xeno/droite-{i}.png", (128, 128), transparente=True)
        assets['xeno_droite'].append(frame)

    assets['xeno_gauche']=[]
    for i in range(10):
        frame= texture(f"xeno/gauche-{i}.png", (128, 128), transparente=True)
        assets['xeno_gauche'].append(frame)






    son_mun = pygame.mixer.Sound("ressource/ESM_Handful_of_Bullet_Shell_Drop_2_Gun_Military_Pistol_Shot_Machine_Rifle_Metal.wav")
    son_pist = pygame.mixer.Sound("ressource/GunshotRevolver_BW.57313.wav")
    son_pomp = pygame.mixer.Sound("ressource/STCR2_PHONK_Kit_One_Shot_TurboCharger_Gunshot (1) (mp3cut.net).mp3")
    son_ass = pygame.mixer.Sound("ressource/GunshotRifle_BW.57890.wav")

    son_mun.set_volume(0.8)
    son_pist.set_volume(0.6)
    son_pomp.set_volume(0.6)
    son_ass.set_volume(0.6)

    #Charger les sons
    assets['son_munition'] = son_mun
    assets['son_pistolet'] = son_pist
    assets['son_pompe'] = son_pomp
    assets['son_assaut'] = son_ass
    
    #Charger les musiques
    assets['musique_menu'] = "ressource/Musique.mp3"
    assets['musique_jeu'] = "ressource/explo.mp3"
    assets['musique_combat'] = "ressource/horrorfight.mp3"
    
    img_etoile = pygame.Surface((Z,Z)).convert()
    img_etoile.fill((5,5,20))
    pygame.draw.circle(img_etoile, (255,255,255), (ZOOM//2,ZOOM//2), 2)
    img_flamme = pygame.Surface((Z,Z)).convert()
    img_flamme.fill((255,69,0))
    assets['img_etoile'] = img_etoile
    assets['img_flamme'] = img_flamme

    voix = {}
    for i in range(7):
        chemin = f"ressource/voix{i}.wav"
        if os.path.exists(chemin):
            voix[i] = pygame.mixer.Sound(chemin)
            voix[i].set_volume(1)
    assets['voix'] = voix


    return assets
ASSETS = None