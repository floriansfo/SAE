import pygame
from prerequis import texture, ZOOM

def charger_assets(largeur, hauteur):
    assets = {}
    Z = ZOOM+1
    #Charger les textures
    assets['img_sol'] = texture("sol.png",(Z,Z))
    assets['img_ascenseur'] = texture("ascenseur.png",(Z,Z))
    assets['img_murface'] = texture("murface.png", (Z, Z))
    assets['img_murtop'] = texture("murtop.png", (Z, Z))
    assets['img_lit'] = texture("lit.png", (Z, Z))
    assets['img_boutique'] = texture("boutique.png", (Z, Z))
    assets['img_logo'] = texture("logormbg.png", (Z, Z))
    assets['img_caisse'] = texture("caisse.png", (Z, Z))
    assets['img_plante'] = texture("plante.png", (Z, Z))
    assets['img_meuble'] = texture("meuble.png", (Z, Z))
    assets['img_lampe'] = texture("lampe.png", (Z, Z))

    assets['img_load'] = texture("Chargement.png", (largeur, hauteur))
    assets['img_piece'] = texture("piece.png", (40,40), transparente=True)
    assets['img_larry'] = texture("Larryv2.png", (200,200), transparente=True)
    assets['img_munition'] = texture("munitionoverlay.png", (80,80), transparente=True)
    assets['img_ballevol'] = texture("balle.png", (45,45), transparente=True)

    assets['img_arme'] = {
        1: texture("pistolet.png",(250,80), transparente= True),
        2: texture("pompe.png",(250,80), transparente= True),
        3: texture("fusil.png",(250,80), transparente= True)
    }
    assets['animationjoueur'] = [
    texture("joueur.png",(100,100), transparente=True),
    texture("joueurgauche.png",(100,100), transparente=True),
    texture("joueurdroit.png",(100,100), transparente=True)
    ]

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

    return assets
ASSETS = None