import pygame
import math
#mode combat
m_combat =False
combat = False
DUREEMODE = 20*60
DUREEDESAC = 50*60
tempscombat = 0
tempsdesac = 0
#obscurité
obscurité_nv=0

def activation_mc(event):
    global m_combat, combat, tempscombat, tempsdesac
    if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
        if not m_combat and tempsdesac <= 0:
            m_combat = True
            combat = True
            tempscombat = DUREEMODE
            tempsdesac = 0

def updatemode():
    global m_combat, combat, tempscombat, tempsdesac
    if m_combat:
        tempscombat -= 1
        if tempscombat <=0:
            tempscombat = 0
            m_combat = False
            combat = True
            tempsdesac = DUREEDESAC
    elif tempsdesac > 0:
            tempsdesac -= 1

def tempsdesactive():
    if tempsdesac >0:
        return tempsdesac/DUREEDESAC
    return 0.0

def tempsmode():
    if m_combat:
        return tempscombat/DUREEMODE
    return 0.0

def filtre(fenetre):
    if m_combat== True:
        L, l= fenetre.get_size()
        surface= pygame.Surface((L, l), pygame.SRCALPHA)
        surface.fill((120, 0, 0, 50))
        fenetre.blit(surface,(0,0))
    
hallucinationactive = False
def hallucination(ecran):
    #Ecran tremble et violet quand oxy < 20
    if hallucinationactive:
        largeur, hauteur = ecran.get_size()
        temps = pygame.time.get_ticks()
        #Flou alterne
        flou = int(100+math.sin(temps*0.005)*50)
        fond = pygame.Surface((largeur, hauteur))
        fond.fill((40,0,20))
        fond.set_alpha(flou)
        ecran.blit(fond, (0,0))

def desactive():
    global m_combat, combat, tempscombat, tempsdesac
    if m_combat:
        m_combat = False
        combat = True
        tempscombat = 0
        tempsdesac = 0