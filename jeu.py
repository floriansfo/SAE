import pygame
import sys
import option
import ascenseur
import pause
import socket
import pickle
import filtre
import overlay
import monstre
import random
import math
import sauvegarde
import nuit
import boutique
import assets
import reseau
import affichage

from prerequis import *
from lumiere import Lumiere
from cartegen import generemap, generer_objets, tango, Objet
from vaisseau import generer_vaisseau
from joueur import Joueur
from vaisseau import LIT, BOUTIQUE

class Partie:
    def __init__(self, ecran, mode="solo", ip = None, save = None):
        self.ecran = ecran
        self.LARGEUR, self.HAUTEUR = ecran.get_size()
        self.mode = mode
        if mode != "solo":
            self.multi = 5.0
        else:
            self.multi = 3.0
        #UI Son
        self.police, self.hudmode, self.hudinventaire, self.inventaire, self.coeur = overlay.overlay_HUD()
        pygame.mixer.music.load(assets.ASSETS['musique_jeu'])
        pygame.mixer.music.play(-1)
        #Serveur
        self.IPSERV = "51.38.115.211"
        self.socket_jeu = None
        self.joueursup = {}
        self.connect = False
        self.buffer = b""
 
        #Si on va pas en solo on lance le multi
        if mode != "solo":
            self.socket_jeu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if mode == "hote":
                print("Mode Hote: Envoi carte au serveur {self.IPSERV}...")
                #Ecran d'attente
                self.ecran.fill((0,0,0))
                font = pygame.font.SysFont("ressource/police.ttf", 36)
                text = font.render("Generation de la carte...", True, (255,255,255))
                self.ecran.blit(text, (self.LARGEUR//2 - 200, self.HAUTEUR//2))
                pygame.display.flip()
                #Configurer le serveur
                try:
                    #Connexion au serveur
                    self.socket_jeu.connect((self.IPSERV, 5555))
                    #Dit au serv qu'on est host
                    self.socket_jeu.send(b"HOST")
                    self.connect = True
                    #L'hote genere la carte avec seed pour clien est meme
                    self.partie = random.randint(0, 999999)
                    random.seed(self.partie)
                    self.carte, self.salles, self.pos = generemap()
                    #Envoie la carte et seed au client
                    data = pickle.dumps({"carte": self.carte, "salles": self.salles, "pos": self.pos, "seed": self.partie})
                    tailledata = len(data).to_bytes(4, byteorder='big')
                    self.socket_jeu.sendall(tailledata + data)
                    #Attend confirme du serv
                    self.socket_jeu.recv(1024)
                    #Generation objet avec seed similaire
                    random.seed(self.partie)
                    self.objets = generer_objets(self.carte, self.salles, self.multi)
                    print("Carte enregistré avec succes")
                except Exception as e:
                    print(f"Erreur de reseau hote: {e}")
            elif mode == "client":
                if ip:
                    cible = ip
                else:
                    cible = self.IPSERV
                print(f"Mode Client: connexion au serveur {cible}...")
                try:
                    #Connexion au serv
                    self.socket_jeu.connect((cible, 5555))
                    #On dit au serv qu'on esy Client
                    self.socket_jeu.send(b"CLIENT")
                    self.connect = True
                    print("Chargement de la carte..")
                    #Reçoit la carte de l'hote
                    taillerecu = self.socket_jeu.recv(4)
                    tailledata = int.from_bytes(taillerecu, byteorder='big')
                    #Telechargement de la carte
                    paquets = []
                    recu = 0
                    while recu < tailledata:
                        paquet = self.socket_jeu.recv(min(4096, tailledata - recu))
                        if not paquet:
                            raise Exception("Connexion perdue")
                        paquets.append(paquet)
                        recu += len(paquet)
                    #Decodage de la carte reçue
                    data = b''.join(paquets)
                    donneesmap = pickle.loads(data)
                    self.carte = donneesmap["carte"]
                    self.salles = donneesmap["salles"]
                    self.pos = donneesmap["pos"]
                    #Application de la seed pour avoir meme objet
                    self.partie = donneesmap["seed"]
                    random.seed(self.partie)
                    self.objets = generer_objets(self.carte, self.salles, self.multi)
                except Exception as e:
                    print(f"Erreur de chargement de la carte: {e}")
            if self.socket_jeu:
            #Empeche le jeu de buger quand on attend un mess reseau
                self.socket_jeu.setblocking(False)
        else:
            #Partie solo
            if save:
                self.partie = save["seed"]
            else:
                self.partie = random.randint(0, 999999)
            if save:
                chargeetage = save["niveau_actuel"]
            else:
                chargeetage = 0
            if chargeetage == 0:
                self.carte, self.salles, self.pos = generer_vaisseau()
                self.objets = generer_objets(self.carte, [], 0)
            else:
                random.seed(self.partie+chargeetage)
                self.carte, self.salles, self.pos = generemap()
                self.objets = generer_objets(self.carte, self.salles, self.multi)

        #Assets et menu
        self.animationjoueur = assets.ASSETS['animationjoueur']
        self.lumieremarche = Lumiere(self.LARGEUR, self.HAUTEUR)
        self.menu = ascenseur.Ascenseur(self.LARGEUR, self.HAUTEUR)
        self.menupause = pause.EcranPause(self.LARGEUR, self.HAUTEUR)
        self.menusommeil = nuit.Sommeil(self.LARGEUR, self.HAUTEUR)
        self.menuboutique = boutique.Boutique(self.LARGEUR, self.HAUTEUR)
        #Parametre Boutique
        self.surboutique = False
        self.boutiqueouverte = False
        self.piecessol = []
        #Parametre temps
        self.jour = 1
        self.heure = 0
        self.enpause = False
        #Parametre ascenceur
        self.ouvertemenu = False
        self.surascenceur = False
        self.sauvegarde_etage = {}
        self.niveau_actuel = 0
        self.modifs_etage = {}
        self.sauvegarde_etage[0] = {"carte": self.carte, "salles": self.salles, "objets": self.objets, "pos": self.pos}
        #Joueur
        px, py = int(self.pos[0]), int(self.pos[1])
        self.joueur = Joueur(px*ZOOM+(ZOOM//2), py*ZOOM+(ZOOM//2))

        #Restauration depuis une sauvegarde
        if save:
            modifs_etage = {int(k): v for k, v in save["modifs"].items()}
            self.joueur.rect.centerx = save["joueur"]["x"]
            self.joueur.rect.centery = save["joueur"]["y"]
            self.joueur.hp = save["joueur"]["hp"]
            self.joueur.munition = save["joueur"]["munition"]
            self.joueur.arsenal = save["joueur"]["arsenal"]
            self.joueur.endurance = save["joueur"]["endurance"]
            self.objets = sauvegarde.appliquer_modifs(self.objets, self.modifs_etage.get(0, {}))
            self.sauvegarde_etage[0]["objets"] = self.objets
            if save["niveau_actuel"] != 0:
                self.niveau_actuel = save["niveau_actuel"]
                random.seed(self.partie + self.niveau_actuel)
                self.carte, self.salles, self.pos = generemap()
                self.objets = generer_objets(self.carte, self.salles, self.multi)
                self.objets = sauvegarde.appliquer_modifs(self.objets, self.modifs_etage.get(self.niveau_actuel, {}))

        self.monstres = []
        self.font = pygame.font.Font("ressource/police.ttf",24)
        self.fonttitre = pygame.font.Font("ressource/police.ttf",36)
        self.fondu = 255
        self.txtvictoire = self.font.render("VICTOIRE RETOUR SUR TERRE", True, (0,255,0))
        self.txtgameover = self.font.render("GAME OVER", True, (255,0,0))
        self.menubtn = self.font.render("MENU", True, (255,255,255))
        self.txtrespawn = self.font.render("RETOUR AU VAISSEAU", True, (255,255,25))
        self.txtinteragir = self.font.render("Appuyez sur E pour interagir", True, (255,255,255))
        self.txtdormir = self.font.render("Appuyer sur E pour dormir", True, (255,255,255))
        self.txtentrer = self.font.render("Appuyer sur E pour entrer", True, (255,255,255))

        def fondtr(txtsurface):
            rect = txtsurface.get_rect()
            fond = pygame.Surface((rect.width+20, rect.height+10), pygame.SRCALPHA)
            fond.fill((0,0,0,150))
            return fond
        
        self.fondinteragir = fondtr(self.txtinteragir)
        self.fonddormir = fondtr(self.txtdormir)
        self.fondentrer = fondtr(self.txtentrer)

        self.pieceinv = -1
        self.imgpiece = None
        self.armeprec = self.joueur.arsenal
        self.glissement = 0
        self.actionmap = {}
        self.mort = False
        self.sonmun = assets.ASSETS['son_munition']
        self.sonmun.set_volume(0.8)
        #Cristal et victoire
        self.cristal_y = None
        self.cristal_x = None
        self.cristaletage = 6
        self.victoire = False
        pygame.time.delay(500)
    
    def evenement(self):
        #Vérifie si le joueur est sur un ascenseur
        casex = int(self.joueur.rect.centerx/ZOOM)
        casey = int(self.joueur.rect.centery/ZOOM)
        self.surascenceur = False
        self.surlit = False
        self.surboutique = False
        #Vérifie si le joueur est sur un lit ou boutique ou ascenseur
        if 0 <= casex < LARGEURMAP and 0 <= casey < HAUTEURMAP:
            if self.carte[casey][casex] == ASCENCEUR:
                self.surascenceur = True
            if self.carte[casey][casex] == LIT:
                self.surlit = True
            if self.carte[casey][casex] == BOUTIQUE:
                self.surboutique = True
        if not self.surboutique:
            self.boutiqueouverte = False
        #Si on s'eloigne de l'ascenseur alors on ferme le menu
        if not self.surascenceur:
            self.ouvertemenu = False
        #Moteur vaisseau
        self.surmoteur = False
        if self.niveau_actuel == 0:
            moteurrect = pygame.Rect(int(self.pos[0])*ZOOM - ZOOM*3, int(self.pos[1])*ZOOM, ZOOM*3, ZOOM*2)
            if self.joueur.rect.colliderect(moteurrect):
                self.surmoteur = True
        
        #Evenement clavier
        self.click = False
        for event in pygame.event.get():
            if self.niveau_actuel != 0:
                filtre.activation_mc(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #Ouvre inventaire
                if event.key == pygame.K_LCTRL and not self.enpause:
                    self.inventaire= not self.inventaire
                #Larry spawn
                if event.key == pygame.K_l and self.niveau_actuel != 0:
                    m= monstre.Monstre(self.joueur.rect.centerx+100, self.joueur.rect.centery, 3, 100)
                    self.monstres.append(m)
                #Allume ou eteindre lampe
                if event.key == pygame.K_h:
                    self.joueur.toogle_lumiere()
                    if self.joueur.lumiereallumee and filtre.m_combat:
                        filtre.m_combat = False
                #Pause ou ferme
                if event.key == pygame.K_ESCAPE:
                    if self.ouvertemenu:
                        self.ouvertemenu = False
                    else:
                        self.enpause = not self.enpause
                #Menu ascenceur
                if event.key == pygame.K_e and self.surascenceur:
                    self.ouvertemenu = not self.ouvertemenu
                if event.key == pygame.K_e and self.surlit and self.niveau_actuel==0:
                    self.jour = self.menusommeil.nuit(self.ecran, self.joueur, self.jour)
                    self.heure = 0
                    self.joueur.achatjour = 0
                    self.joueur.oxygene = self.joueur.oxygenemax
                if event.key == pygame.K_e and self.surboutique and self.niveau_actuel == 0:
                    self.boutiqueouverte = not self.boutiqueouverte
                if event.key == pygame.K_e and self.surmoteur and self.joueur.cristal:
                    self.victoire = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #Clic gauche
                    self.click = True
                if self.boutiqueouverte:
                    self.menuboutique.clique(pygame.mouse.get_pos(), self.bouton_boutique, self.joueur)

    def msj(self, t):
        mouse_pos = pygame.mouse.get_pos()
        #Mode combat desactive quand tire pas
        if self.niveau_actuel!=0:
            filtre.updatemode()
        if self.victoire:
            self.ecran.fill((0,0,0))
            self.ecran.blit(self.txtvictoire, self.txtvictoire.get_rect(center=(self.LARGEUR//2, self.HAUTEUR//2-100)))
            btn_menu = pygame.Rect(0,0,200,60)
            btn_menu.center = (self.LARGEUR//2, self.HAUTEUR//2+50)
            pygame.draw.rect(self.ecran, (100,100,100) if btn_menu.collidepoint(mouse_pos) else (50,50,50), btn_menu)
            self.ecran.blit(self.menubtn, self.menubtn.get_rect(center=btn_menu.center))
            if self.click and btn_menu.collidepoint(mouse_pos):
                return "MENU"
            return "VICTOIRE"
            
        #Le joueur est mort
        if self.mort:
            self.ecran.fill((0,0,0))
            self.ecran.blit(self.txtgameover, self.txtgameover.get_rect(center=(self.LARGEUR//2, self.HAUTEUR//2-100)))
            if getattr(self.joueur, "cristal", False):
                self.joueur.cristal = False
                self.cristaletage = self.niveau_actuel
                self.cristal_x = self.joueur.rect.centerx
                self.cristal_y = self.joueur.rect.centery
            btn_respawn = pygame.Rect(0,0,350,60)
            btn_respawn.center = (self.LARGEUR//2, self.HAUTEUR//2+50)
            pygame.draw.rect(self.ecran, (100,100,100) if btn_respawn.collidepoint(mouse_pos) else (50,50,50), btn_respawn)
            self.ecran.blit(self.txtrespawn, self.txtrespawn.get_rect(center=btn_respawn.center))
            if self.click and btn_menu.collidepoint(mouse_pos):
                self.mort = False
                self.joueur.hp = self.joueur.hpmax
                self.niveau_actuel = 0
                self.carte, self.salles, self.pos = generer_vaisseau()
                self.objets = generer_objets(self.carte, [], 0)
                self.joueur.rect.center = (int(self.pos[0])*ZOOM+(ZOOM//2), int(self.pos[1])*ZOOM+(ZOOM//2))
                self.monstres= []
                self.joueur.possedelampe = True
                return "CONTINUER"
            return "MORT"
        
        if not self.ouvertemenu and not self.enpause:
            keys = pygame.key.get_pressed()
            #Deplacement joueur et collision
            kx, ky = self.joueur.deplacer(keys, len(self.animationjoueur), t)
            self.joueur.collision(kx, ky, self.carte, self.objets)
            self.joueur.updatelampe(filtre.m_combat)
            #Changement arme
            if keys[pygame.K_1]:
                self.joueur.changerarme(1)
            if keys[pygame.K_2] and self.joueur.arsenal_achete.get(2, False):
                self.joueur.changerarme(2)
            if keys[pygame.K_3] and self.joueur.arsenal_achete.get(3, False):
                self.joueur.changerarme(3)
            #Ramasser munition
            objetsreste = []
            for obj in self.objets:
                if obj.type == "munition" and self.joueur.rect.colliderect(obj.rect):
                    self.joueur.munition = self.joueur.munition + 15
                    self.sonmun.play()
                    key = f"{obj.rect.x}-{obj.rect.y}"
                    self.actionmap[key] = "S"
                    self.modifs_etage.setdefault(self.niveau_actuel, {})[key] = "S"
                elif obj.type == "cristal" and self.joueur.rect.colliderect(obj.rect):
                    self.joueur.cristal = True
                    self.sonmun.play()
                    key = f"{obj.rect.x}-{obj.rect.y}"
                    self.actionmap[key]="S"
                    self.modifs_etage.setdefault(self.niveau_actuel, {})[key]="S"
                    px,py = int(self.pos[0]), int(self.pos[1])
                    self.monstres.append(monstre.Titan(px*ZOOM+ZOOM, py*ZOOM+ZOOM))    
                else:
                    objetsreste.append(obj)
            self.objets = objetsreste #Met a jour les objets restants
            #Ramasser piece
            piecesreste = []
            for p in self.piecessol:
                if self.joueur.rect.colliderect(p["rect"]):
                    self.joueur.pieces += p["valeur"]
                else:
                    piecesreste.append(p)
            self.piecessol = piecesreste #Met a jour les pieces restantes
            #Monstre loot piece
            monstresvivant = []
            for m in self.monstres:
                if m.mort:
                    if getattr(m, "loot", 0) > 0:
                        self.piecessol.append({"rect": pygame.Rect(m.rect.centerx-20, m.rect.centery-20, 40, 40), "valeur": m.loot})
                else:
                    monstresvivant.append(m)
            self.monstres = monstresvivant
            #Tir
            if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and self.niveau_actuel != 0:
                self.joueur.tirer()
            #Deplacement balle et acutalisation caisse cassé
            casse = self.joueur.updatetir(self.carte, self.objets, self.monstres, t)
            if casse:
                for c in casse:
                    key = f"{c.rect.x}-{c.rect.y}"
                    self.actionmap[key] = "M"
                    self.modifs_etage.setdefault(self.niveau_actuel, {})[key] = "M"
            #Si en dehor de l'ecran on stop le mouvement
            if self.joueur.god > 0:
                self.joueur.god -= 60*t
            #Deplacement provisoire
            for m in self.monstres:
                if not m.mort :
                    if getattr(m, "traque", False) or abs(m.rect.centerx - self.joueur.rect.centerx) < self.LARGEUR and abs(m.rect.centery - self.joueur.rect.centery) < self.HAUTEUR:
                        kx, ky = m.deplacement(t, self.joueur.rect.centerx, self.joueur.rect.centery)
                        m.collision(kx, ky, self.carte, self.objets)
                        #le monstre touche le joueur
                        if m.rect.colliderect(self.joueur.rect) and self.joueur.god<=0:
                            degat = getattr(m, "degats", 10)
                            self.joueur.hp -= degat
                            self.joueur.god= 60
                            if self.joueur.hp <= 0:
                                self.mort = True
                                self.joueur.possedelampe = False
                                self.joueur.lumiereallumee = False
            #Oxygene
            self.joueur.updateoxygene(self.niveau_actuel)
            if self.joueur.hp <=0 and not self.mort:
                self.mort = True
            #Heure
            if self.niveau_actuel != 0:
                self.heure += 60*t
                if self.heure >= 28800:
                    if not hasattr(self.joueur, "time"):
                        self.joueur.time = 0
                    self.joueur.time += 60*t
                    if self.joueur.time >= 120:
                        self.joueur.time = 0
                        self.joueur.hp = self.joueur.hp - 5
                        if self.joueur.hp <= 0:
                            self.mort = True
                            self.joueur.possedelampe = False
                            self.joueur.lumiereallumee = False 
            #Reseau
        if self.connect:
            self.buffer, self.objets, self.joueursup = reseau.connexion(self.socket_jeu, self.joueur, self.monstres, self.objets, self.actionmap, self.mort, self.niveau_actuel, self.buffer, self.joueursup)   
        return "CONTINUER"
    
    def menus(self):
        #Message sur ascenseur
        if self.surascenceur and not self.ouvertemenu:
            txt_rect = self.txtinteragir.get_rect(center=(self.LARGEUR//2, self.HAUTEUR-50))
            self.ecran.blit(self.fondinteragir,(txt_rect.x-10, txt_rect.y-5))
            self.ecran.blit(self.txtinteragir, txt_rect)
        #Message pour le lit
        if self.surlit and not self.ouvertemenu and self.niveau_actuel == 0:
            tx_rect = self.txtdormir.get_rect(center=(self.LARGEUR//2, self.HAUTEUR-50))
            self.ecran.blit(self.fonddormir,(tx_rect.x-10, tx_rect.y-5))
            self.ecran.blit(self.txtdormir, tx_rect)
        #Message pour la boutique
        if self.surboutique and not self.boutiqueouverte and self.niveau_actuel == 0:
            t_rect = self.txtentrer.get_rect(center=(self.LARGEUR//2, self.HAUTEUR-50))
            self.ecran.blit(self.fondentrer,(t_rect.x-10, t_rect.y-5))
            self.ecran.blit(self.txtentrer, t_rect)

        #Menu boutique ascenseur 
        self.bouton_boutique = []
        if self.ouvertemenu:
            menu_boutons = self.menu.dessiner(self.ecran, self.niveau_actuel, self.joueur)
            if self.click:
                etage_choisi = self.menu.clique(pygame.mouse.get_pos(), menu_boutons)
                if etage_choisi is not None:
                    self.sauvegarde_etage[self.niveau_actuel] = {
                        "carte": self.carte,
                        "salles": self.salles,
                        "objets": self.objets,
                        "pos": self.pos,
                    }
                    self.menu.ecran_charge(self.ecran, assets.ASSETS['img_load'], etage_choisi)
                    #Si l'étage a déjà été visité, on charge la sauvegarde
                    if etage_choisi in self.sauvegarde_etage:
                        self.carte = self.sauvegarde_etage[etage_choisi]["carte"]
                        self.salles = self.sauvegarde_etage[etage_choisi]["salles"]
                        self.objets = self.sauvegarde_etage[etage_choisi]["objets"]
                        self.pos = self.sauvegarde_etage[etage_choisi]["pos"]
                    else:
                        if etage_choisi == 0:
                            #Toujours vaisseau
                            self.carte, self.salles, self.pos = generer_vaisseau()
                            self.objets = generer_objets(self.carte, [], 0)
                        elif 1<= etage_choisi <=6:
                            #Nouvelle carte
                            random.seed(self.partie+etage_choisi)
                            self.carte, self.salles, self.pos = generemap()
                            self.objets = generer_objets(self.carte, self.salles, self.multi)
                            self.objets = sauvegarde.appliquer_modifs(self.objets, self.modifs_etage.get(etage_choisi, {}))
                    self.niveau_actuel = etage_choisi
                    #Si etage 6 on active quete
                    if self.niveau_actuel == self.cristaletage and not getattr(self.joueur, "cristal", False):
                        if self.cristal_x is None and self.cristaletage == 6:
                            objtang, posc = tango(self.carte, self.salles, poscristal=True)
                            if objtang:
                                self.objets.extend(objtang)
                        elif self.cristal_x is not None:
                            self.objets.append(Objet(self.cristal_x, self.cristal_y, "cristal.png", "cristal", size=(ZOOM//2, ZOOM//2)))
                    if getattr(self.joueur, "cristal", False) and self.niveau_actuel != 0:
                        posx, posy = int(self.pos[0]), int(self.pos[1])
                        self.monstres.append(monstre.Titan(posx*ZOOM+ZOOM*2, posy*ZOOM+ZOOM*2))
                    #Repositionne le joueur sur la nouvelle carte a l"ascenseur
                    posx,posy = int(self.pos[0]), int(self.pos[1])
                    self.joueur.rect.center = (posx*ZOOM+(ZOOM//2), posy*ZOOM+(ZOOM//2))
                    pygame.time.delay(500)
                    self.ouvertemenu = False
                    pygame.event.clear()
        if self.boutiqueouverte:
            self.bouton_boutique = self.menuboutique.dessiner(self.ecran, self.joueur)
        #Menu pause
        if self.enpause:
            boutons = self.menupause.dessiner(self.ecran)
            if self.click:
                action = self.menupause.clique(pygame.mouse.get_pos(), boutons)
                if action == "REPRENDRE":
                    self.enpause = False
                elif action == "SAUVEGARDER":
                    self.sauvegarde_etage[self.niveau_actuel] = {
                        "carte": self.carte,
                        "salles": self.salles,
                        "objets": self.objets,
                    }
                    sauvegarde.sauvegarder(self.partie, self.niveau_actuel, self.modifs_etage, self.joueur)
                elif action == "OPTIONS":
                    self.ecran = option.option_menu(self.ecran, self.LARGEUR, self.HAUTEUR)
                    self.LARGEUR, self.HAUTEUR = self.ecran.get_size()
                    #Met a jour les res de tout le jeu
                    self.menupause.update_dimensions(self.LARGEUR, self.HAUTEUR)
                    self.menu.update_dimensions(self.LARGEUR, self.HAUTEUR)
                    img_load = pygame.transform.scale(assets.ASSETS['img_load'], (self.LARGEUR,self.HAUTEUR))
                elif action == "MENU PRINCIPAL":
                    return "MENU" #Revenir au menu principal
                elif action == "QUITTER":
                    pygame.quit()
                    sys.exit()
        return "CONTINUER"
    
    def dessine(self):
        #Musique mode combat
        if filtre.combat:
            if self.niveau_actuel != 0:
                if filtre.m_combat:
                    #Active nouvelle sic
                    pygame.mixer.music.load(assets.ASSETS['musique_combat'])
                    pygame.mixer.music.play(-1)
                else:
                    #Met ancienne sic
                    pygame.mixer.music.load(assets.ASSETS['musique_jeu'])
                    pygame.mixer.music.play(-1)
            filtre.combat = False
        affichage.dessinerjeu(self.ecran, self.LARGEUR, self.HAUTEUR, self.carte, self.joueur, self.objets, self.piecessol, self.monstres, self.joueursup, self.niveau_actuel, self.connect, self.lumieremarche, filtre)
        if self.menus() == "MENU":
            return "MENU"
        #Overlay
        if not self.enpause:
            touche = pygame.key.get_pressed()
            mouvement = any(touche[k] for k in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP,pygame.K_DOWN, pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d])
            course = mouvement and touche[pygame.K_LSHIFT] and self.joueur.endurance > 0
            #Apparition fondu de la barre
            if not course and self.joueur.endurance >= self.joueur.maxcourse:
                self.fondu = max(0, self.fondu-5)
            else:
                self.fondu = min(255, self.fondu+25)   
            overlay.endurance(self.ecran, self.joueur, course, self.HAUTEUR, self.LARGEUR)
            overlay.munition(self.ecran, self.joueur, self.police, assets.ASSETS['img_munition'], self.HAUTEUR)
            #Arme overlay
            #Si changement d'arme on glisse image
            if self.joueur.arsenal != self.armeprec:
                self.armeprec = self.joueur.arsenal
                self.glissement = -400
            if self.glissement < 0:
                self.glissement += 35
                if self.glissement > 0:
                    self.glissement = 0
            overlay.arme_overlay(self.ecran, self.joueur, assets.ASSETS['img_arme'], self.HAUTEUR, self.glissement)
            overlay.lampe(self.ecran, self.joueur, self.font, assets.ASSETS.get('img_lampe'), self.HAUTEUR)
            if self.niveau_actuel!=0:
                overlay.oxygene(self.ecran, self.joueur, self.font, self.LARGEUR, self.HAUTEUR)
            overlay.hud_life(self.ecran, self.LARGEUR, self.HAUTEUR, self.joueur.hp, self.joueur.hpmax, self.police, self.coeur)
            overlay.pieces(self.ecran, self.joueur, self.font, self.LARGEUR)
            overlay.horloge(self.ecran, self.font, self.jour, self.heure, self.LARGEUR)
            overlay.onventaire(self.ecran, self.inventaire, self.hudinventaire, self.LARGEUR, self.HAUTEUR)
            filtre.filtre(self.ecran)
        #texte mode overlay
        overlay.mode_texte(self.ecran, filtre.m_combat, self.enpause, self.police, self.hudmode, self.inventaire)                                      
        pygame.display.flip()
        return "CONTINUER"
    
def lancer(ecran, mode="solo", ip = None, save=None):
    partie = Partie(ecran, mode, ip, save)
    clock = pygame.time.Clock()
    running = True
    while running:
        partie.LARGEUR, partie.HAUTEUR = ecran.get_size()
        t = clock.tick(60) / 1000.0
        #Frappe du clavier
        partie.evenement()
        #Calcul
        stat = partie.msj(t)
        if stat == "MENU":
            break
        elif stat == "MORT":
            pygame.display.flip()
            continue
        #Dessine
        statdessin = partie.dessine()
        if statdessin == "MENU":
            break
    if partie.socket_jeu:
        partie.socket_jeu.close()