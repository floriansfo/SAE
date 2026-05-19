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
import moteur
import enregistrement

from prerequis import *
from lumiere import Lumiere
from cartegen import generemap, generer_objets, tango, Objet
from vaisseau import generer_vaisseau
from joueur import Joueur
from vaisseau import LIT, BOUTIQUE
from mimique import Mimique
from nyctobat import Nyctobat
from errant import Errant

class Partie:
    def __init__(self, ecran, mode="solo", ip = None, save = None):
        self.ecran = ecran
        self.LARGEUR, self.HAUTEUR = ecran.get_size()
        self.mode = mode
        if mode != "solo":
            self.multi = 5.0
        else:
            self.multi = 3.0
        #timer
        self.timer_obscurité=0
        #UI Son
        self.overlay = overlay.Overlay(self.LARGEUR, self.HAUTEUR)
        self.inventaire = False
        #Musique
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
                dx, dy = int(self.pos[0]), int(self.pos[1])
                self.objets.append(Objet((dx-2)*ZOOM, dy*ZOOM, "img_cassette", "dialogue", size =(ZOOM//2, ZOOM//2)))
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
        #Moteur vaisseau
        self.moteur = moteur.Moteur(self.LARGEUR, self.HAUTEUR)
        self.moteurouvert = False
        self.dialogue = enregistrement.Enregistrement(self.LARGEUR, self.HAUTEUR)
        self.dialogueouvert = False

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
        self.surmoteur = False
        self.moteurcol = None
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
            largeur = ZOOM*3
            hauteur = ZOOM*1.5
            posx = (int(self.pos[0])-1)*ZOOM
            posy = (int(self.pos[1])-3.5)*ZOOM
            self.moteurcol = pygame.Rect(posx, posy, largeur, hauteur)
            zone = self.moteurcol.inflate(ZOOM, ZOOM)
            if self.joueur.rect.colliderect(zone):
                self.surmoteur = True
        
        #Evenement clavier
        self.click = False
        self.clickdroit = False
        for event in pygame.event.get():
            if self.niveau_actuel != 0:
                filtre.activation_mc(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if getattr(self,"moteurouvert", False):
                self.moteur.gerer_evenements(event, self.joueur)
            if event.type == pygame.KEYDOWN:
                #Ouvre inventaire
                if event.key == pygame.K_LCTRL and not self.enpause:
                    self.inventaire= not self.inventaire
                #Larry spawn
                if event.key == pygame.K_l and self.niveau_actuel != 0:
                    m= monstre.Monstre(self.joueur.rect.centerx+100, self.joueur.rect.centery, 3, 100)
                    self.monstres.append(m)
                #mimique spawn
                if event.key == pygame.K_m and self.niveau_actuel != 0:
                    m= Mimique(self.joueur.rect.centerx+500, self.joueur.rect.centery)
                    self.monstres.append(m)
                #Allume ou eteindre lampe
                if event.key == pygame.K_h:
                    self.joueur.toogle_lumiere()
                    if self.joueur.lumiereallumee and filtre.m_combat:
                        filtre.m_combat = False
                #Pause ou ferme
                if event.key == pygame.K_ESCAPE:
                    if self.dialogue.ouvert:
                        self.dialogue.fermer()
                    elif getattr(self,"moteurouvert", False):
                        self.moteurouvert = False
                    elif getattr(self, "ouvertemenu", False):
                        self.ouvertemenu = False
                    elif getattr(self, "boutiqueouverte", False):
                        self.boutiqueouverte = False
                    elif getattr(self, "inventaire", False):
                        self.inventaire = False
                    else:
                        self.enpause = not self.enpause
                #Menu ascenceur
                if event.key == pygame.K_e:
                    if getattr(self,"dialogueouvert", False) and not self.dialogue.ouvert:
                        self.dialogue.ouvrir(self.niveau_actuel)
                    if self.surascenceur:
                        self.ouvertemenu = True
                    if self.surlit and self.niveau_actuel==0:
                        self.menusommeil.dodo(self.joueur, self.jour, self.heure)
                    if self.surboutique and self.niveau_actuel == 0:
                        self.boutiqueouverte = True
                    #Ouvre le moteur si on fait E
                    if self.surmoteur:
                        self.moteurouvert = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #Clic gauche
                    self.click = True
                if event.button == 3: #Clic droit
                    self.clickdroit = True
                if getattr(self, "boutiqueouverte", False):
                    pieceav = self.joueur.pieces
                    munav = self.joueur.munition
                    arseav = list(self.joueur.arsenal_achete.keys())
                    self.menuboutique.clique(pygame.mouse.get_pos(), self.bouton_boutique, self.joueur)
                    if self.joueur.pieces < pieceav:
                        perte= pieceav - self.joueur.pieces
                        if hasattr(self.joueur, "retirer"):
                            self.joueur.retirer("piece", perte)
                    if self.joueur.munition > munav:
                        g = self.joueur.munition - munav
                        self.joueur.munition = munav
                        if hasattr(self.joueur, "quantite"):
                            reste = self.joueur.quantite("munition", g)
                            self.joueur.munition += (g - reste)
                            if reste > 0:
                                px = self.joueur.rect.centerx+random.randint(-40,40)
                                py = self.joueur.rect.centery+random.randint(-40,40)
                                objsur = Objet(px, py, "img_munition", "munition", size=(40,40))
                                objsur.quantite = reste
                                self.objets.append(objsur)
                    for num in list(self.joueur.arsenal_achete.keys()):
                        if num not in arseav:
                            nom = {0: "couteau", 1: "pistolet", 2: "pompe", 3: "fusil"}
                            armeachete = nom.get(num)
                            if armeachete and hasattr(self.joueur, "quantite"):
                                reste = self.joueur.quantite(armeachete, 1)
                                if reste >0:
                                    px = self.joueur.rect.centerx+random.randint(-40,40)
                                    py = self.joueur.rect.centery+random.randint(-40,40)
                                    objsur = Objet(px, py, f"img_{armeachete}", armeachete, size=(40,40))
                                    objsur.quantite = 1
                                    self.objets.append(objsur)

    def msj(self, t):
        mouse_pos = pygame.mouse.get_pos()
        #Mode combat desactive quand tire pas
        if self.niveau_actuel!=0:
            filtre.updatemode()
        else:
            filtre.desactive()
        #Victoire
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
            if self.click and btn_respawn.collidepoint(mouse_pos):
                self.mort = False
                self.joueur.hp = self.joueur.hpmax
                self.niveau_actuel = 0
                self.carte, self.salles, self.pos = generer_vaisseau()
                self.objets = generer_objets(self.carte, [], 0)
                self.joueur.rect.center = (int(self.pos[0])*ZOOM+(ZOOM//2), int(self.pos[1])*ZOOM+(ZOOM//2))
                self.monstres= []
                self.joueur.possedelampe = False
                self.joueur.lumiereallumee = False
                filtre.desactive()
                return "CONTINUER"
            return "MORT"
        
        if not self.ouvertemenu and not self.enpause and not getattr(self,"moteurouvert", False) and not self.menusommeil.cours and not self.boutiqueouverte:
            #diminution du noir
            self.timer_obscurité+=1
            if self.timer_obscurité>5:
                self.timer_obscurité=0
                if filtre.obscurité_nv>0:
                    filtre.obscurité_nv-=1
            keys = pygame.key.get_pressed()
            #Racine ralenti
            rx = int(self.joueur.rect.centerx/ZOOM)
            ry = int(self.joueur.rect.centery/ZOOM)
            ralenti = False
            if 0 <= rx < LARGEURMAP and 0 <= ry < HAUTEURMAP:
                if self.carte[ry][rx] == 9:
                    ralenti = True
                    if self.niveau_actuel != 0:
                        self.joueur.hp -= 2*t
                        if self.joueur.hp <= 0 and not self.mort:
                            self.mort = True
                            self.joueur.possedelampe = False
                            self.joueur.lumiereallumee = False
            #Deplacement joueur et collision
            rapidite = (t/2) if ralenti else t
            kx, ky = self.joueur.deplacer(keys, len(self.animationjoueur), rapidite)
            self.joueur.collision(kx, ky, self.carte, self.objets, getattr(self,"moteurcol", None))
            self.joueur.updatelampe(filtre.m_combat)
            #Changement arme
            if keys[pygame.K_1]:
                self.joueur.changerarme(0)
            if keys[pygame.K_2]:
                self.joueur.changerarme(1)
            if keys[pygame.K_3]:
                self.joueur.changerarme(2)
            if keys[pygame.K_4]:
                self.joueur.changerarme(3)
            #Ramasser munition
            objetsreste = []
            self.dialogueouvert = False
            for obj in self.objets:
                if obj.type == "munition" and self.joueur.rect.colliderect(obj.rect):
                    qte = getattr(obj, "quantite", 15)
                    reste = self.joueur.quantite("munition", qte)
                    ga = qte - reste
                    self.joueur.munition += ga
                    if reste > 0:
                        obj.quantite -= reste
                        objetsreste.append(obj)
                    else:
                        k = f"{obj.rect.x}-{obj.rect.y}"
                        self.actionmap[k] = "S"
                        self.modifs_etage.setdefault(self.niveau_actuel, {})[k] = "S"
                    self.sonmun.play()
                elif obj.type in ["couteau", "pistolet", "pompe", "fusil"] and self.joueur.rect.colliderect(obj.rect):
                    qte = getattr(obj, "quantite", 1)
                    reste = self.joueur.quantite(obj.type, qte)
                    if reste>0:
                        obj.quantite = reste
                        objetsreste.append(obj)
                    else:
                        k = f"{obj.rect.x}-{obj.rect.y}"
                        self.actionmap[k] = "S"
                        self.modifs_etage.setdefault(self.niveau_actuel, {})[k] = "S"
                elif obj.type == "cristal" and self.joueur.rect.colliderect(obj.rect):
                    self.joueur.cristal = True
                    if hasattr(self.joueur, "quantite"):
                        self.joueur.quantite("cristal", 1)
                    self.sonmun.play()
                    key = f"{obj.rect.x}-{obj.rect.y}"
                    self.actionmap[key]="S"
                    self.modifs_etage.setdefault(self.niveau_actuel, {})[key]="S"
                    px,py = int(self.pos[0]), int(self.pos[1])
                    self.monstres.append(monstre.Titan(px*ZOOM+ZOOM, py*ZOOM+ZOOM))    
                elif obj.type == "dialogue" and self.joueur.rect.colliderect(obj.rect):
                    self.dialogueouvert = True
                    objetsreste.append(obj)
                else:
                    objetsreste.append(obj)
            self.objets = objetsreste #Met a jour les objets restants
            #Ramasser piece
            piecesreste = []
            for p in self.piecessol:
                if self.joueur.rect.colliderect(p["rect"]):
                    reste = self.joueur.quantite("piece", p["valeur"])
                    ga = p["valeur"] - reste
                    self.joueur.pieces += ga
                    if reste > 0:
                        p["valeur"] = reste
                        piecesreste.append(p)
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
            for m in self.monstres:
                if isinstance(m, monstre.Titan):
                    if m.hp < 99999:
                        m.recule = 2.0
                        m.hp = 99999
                        m.rect.x += 15 if self.joueur.rect.centerx < m.rect.centerx else -15
            #Si en dehor de l'ecran on stop le mouvement
            if self.joueur.god > 0:
                self.joueur.god -= 60*t
            #Deplacement provisoire
            if self.niveau_actuel != 0:
                for m in self.monstres:
                    if not m.mort :
                        if isinstance(m, Mimique):
                            m.comportement(t,[self.joueur])
                        if isinstance(m, Nyctobat):
                            m.comportement(t, [self.joueur])
                        if isinstance(m, Errant):
                            m.comportement(t, [self.joueur])
                        if isinstance(m, monstre.Titan):
                            m.lampejoueur = self.joueur.lumiereallumee
                        if getattr(m, "traque", False) or abs(m.rect.centerx - self.joueur.rect.centerx) < self.LARGEUR and abs(m.rect.centery - self.joueur.rect.centery) < self.HAUTEUR:
                            kx, ky = m.deplacement(t, self.joueur.rect.centerx, self.joueur.rect.centery)
                            m.collision(kx, ky, self.carte, self.objets)
                            #le monstre touche le joueur
                            if m.rect.colliderect(self.joueur.rect) and self.joueur.god<=0:
                                degat = getattr(m, "degats", 10)
                                self.joueur.hp -= degat
                                self.joueur.god= 60
                                if isinstance(m, Nyctobat):
                                    filtre.obscurité_nv +=40
                                    if filtre.obscurité_nv>255:
                                        filtre.obcurité_nv=255
                                if self.joueur.hp <= 0:
                                    self.mort = True
                                    self.joueur.possedelampe = False
                                    self.joueur.lumiereallumee = False
            #Oxygene
            self.joueur.updateoxygene(self.niveau_actuel)
            if getattr(self.joueur, "oxygene", 100) < getattr(self.joueur, "oxygenemax", 100)*0.20 and self.niveau_actuel != 0:
                filtre.hallucinationactive = True
                #Hallucination tir
                if random.random() < 0.02:
                    sonhallucination = assets.ASSETS.get('son_pistolet')
                    son = pygame.mixer.find_channel()
                    son.set_volume(0.3)
                    son.play(sonhallucination)
            else:
                filtre.hallucinationactive = False

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
        #Message pour le moteur
        if getattr(self,"surmoteur", False) and not getattr(self,"moteurouvert", False) and self.niveau_actuel == 0:
            texterect = self.txtinteragir.get_rect(center=(self.LARGEUR//2, self.HAUTEUR-50))
            self.ecran.blit(self.fondinteragir,(texterect.x-10, texterect.y-5))
            self.ecran.blit(self.txtinteragir, texterect)
        #Message pour dialogue
        if getattr(self,"dialogueouvert", False) and not self.dialogue.ouvert:
            txtrect = self.txtinteragir.get_rect(center=(self.LARGEUR//2, self.HAUTEUR-50))
            self.ecran.blit(self.fondinteragir,(txtrect.x-10, txtrect.y-5))
            self.ecran.blit(self.txtinteragir, txtrect)

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
                            dx, dy = int(self.pos[0]), int(self.pos[1])
                            self.objets.append(Objet((dx-2)*ZOOM, dy*ZOOM, "img_cassette", "dialogue", size =(ZOOM//2, ZOOM//2)))
                        elif 1<= etage_choisi <=6:
                            #Nouvelle carte
                            random.seed(self.partie+etage_choisi)
                            self.carte, self.salles, self.pos = generemap()
                            self.objets = generer_objets(self.carte, self.salles, self.multi)
                            self.objets = sauvegarde.appliquer_modifs(self.objets, self.modifs_etage.get(etage_choisi, {}))
                    self.niveau_actuel = etage_choisi
                    
                    self.monstres.clear()
                    self.monstres.extend(monstre.spawn_metage(self.niveau_actuel, self.salles))
                    if self.niveau_actuel == 0:
                        self.joueur.lumiereallumee = False
                        filtre.desactive()
                    #Si etage 6 on active quete
                    if self.niveau_actuel == self.cristaletage and not getattr(self.joueur, "cristal", False):
                        if self.cristal_x is None and self.cristaletage == 6:
                            objtang, posc = tango(self.carte, self.salles, poscristal=True)
                            if objtang:
                                self.objets.extend(objtang)
                        elif self.cristal_x is not None:
                            self.objets.append(Objet(self.cristal_x, self.cristal_y, "cristal.png", "cristal", size=(ZOOM//2, ZOOM//2)))
                    #Spawn titan
                    if self.niveau_actuel == 6 and not getattr(self, "titanspawn", False):
                        self.titanspawn = True
                        px, py = int(self.pos[0]), int(self.pos[1])
                        #Spawn a 10 case de l'ascenceur
                        self.titanla = monstre.Titan(px*ZOOM+ZOOM*10, py*ZOOM+ZOOM*10)
                    #Titan suit dans les etages
                    if getattr(self, "titanla", None) is not None and self.niveau_actuel != 0:
                        px, py= int(self.pos[0]), int(self.pos[1])
                        #Dans les etages on le change
                        self.titanla.rect.centerx = px*ZOOM+ZOOM*10
                        self.titanla.rect.centery = py*ZOOM+ZOOM*10
                        self.monstres.append(self.titanla)
                    #Repositionne le joueur sur la nouvelle carte a l"ascenseur
                    posx,posy = int(self.pos[0]), int(self.pos[1])
                    self.joueur.rect.center = (posx*ZOOM+(ZOOM//2), posy*ZOOM+(ZOOM//2))
                    pygame.time.delay(500)
                    self.ouvertemenu = False
                    pygame.event.clear()
        if self.boutiqueouverte and not self.enpause:
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
                    self.overlay.update_dimensions(self.LARGEUR, self.HAUTEUR)
                    self.moteur.update_dimension(self.LARGEUR, self.HAUTEUR)
                    self.menu.update_dimensions(self.LARGEUR, self.HAUTEUR)
                    self.menuboutique.update(self.LARGEUR, self.HAUTEUR)
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
                if filtre.m_combat and self.niveau_actuel != 0:
                    #Active nouvelle sic
                    pygame.mixer.music.load(assets.ASSETS['musique_combat'])
                    pygame.mixer.music.play(-1)
                else:
                    #Met ancienne sic
                    pygame.mixer.music.load(assets.ASSETS['musique_jeu'])
                    pygame.mixer.music.play(-1)
                filtre.combat = False
        affichage.dessinerjeu(self.ecran, self.LARGEUR, self.HAUTEUR, self.carte, self.joueur, self.objets, self.piecessol, self.monstres, self.joueursup, self.niveau_actuel, self.connect, self.lumieremarche, filtre, getattr(self,"moteurcol", None))
        if self.menus() == "MENU":
            return "MENU"
        #Overlay
        if not self.enpause and not self.dialogue.ouvert:
            touche = pygame.key.get_pressed()
            mouvement = any(touche[k] for k in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP,pygame.K_DOWN, pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d])
            course = mouvement and touche[pygame.K_LSHIFT] and self.joueur.endurance > 0
            #Apparition fondu de la barre
            if not course and self.joueur.endurance >= self.joueur.maxcourse:
                self.fondu = max(0, self.fondu-5)
            else:
                self.fondu = min(255, self.fondu+25)
            self.overlay.endurance(self.ecran, self.joueur, course)
            self.overlay.munition(self.ecran, self.joueur, assets.ASSETS['img_munition'])
            #Arme overlay
            #Si changement d'arme on glisse image
            if self.joueur.arsenal != self.armeprec:
                self.armeprec = self.joueur.arsenal
                self.glissement = -400
            if self.glissement < 0:
                self.glissement += 35
                if self.glissement > 0:
                    self.glissement = 0
            self.overlay.arme_overlay(self.ecran, self.joueur, assets.ASSETS['img_arme'], self.glissement)
            self.overlay.lampe(self.ecran, self.joueur, assets.ASSETS.get('img_lampe'))
            if self.niveau_actuel!=0:
                self.overlay.oxygene(self.ecran, self.joueur)
            self.overlay.hud_life(self.ecran, self.joueur.hp, self.joueur.hpmax)
            self.overlay.pieces(self.ecran, self.joueur)
            self.overlay.horloge(self.ecran, self.jour, self.heure)
            self.overlay.onventaire(self.ecran, self.inventaire)
            filtre.filtre(self.ecran)
            filtre.hallucination(self.ecran)
            if filtre.obscurité_nv>0:
                noir= pygame.Surface(self.ecran.get_size())
                noir.fill((0,0,0))
                noir.set_alpha(filtre.obscurité_nv)
                self.ecran.blit(noir,(0,0))
        #texte mode overlay
        if not self.enpause:
            self.overlay.mode_texte(self.ecran, filtre.m_combat, self.enpause,self.inventaire)                                      
        if self.menusommeil.cours:
            etat = self.menusommeil.dessine(self.ecran, self.joueur)
            if etat == "REVEIL":
                self.jour += 1
                self.heure = 0
                self.joueur.achatjour = 0
                self.joueur.oxygene = self.joueur.oxygenemax
                self.joueur.hp += self.menusommeil.soinpris
        if self.moteurouvert:
            imgdiamant = assets.ASSETS.get('cristal1.png')
            self.moteur.dessiner(self.ecran, self.joueur, imgdiamant)
            if self.moteur.resolu:
                self.victoire = True
                self.moteurouvert = False
        if self.dialogue.ouvert:
            self.dialogue.dessiner(self.ecran)
        if getattr(self, "inventaire", False):
            pos = pygame.mouse.get_pos()
            cliquedroit = getattr(self, "clickdroit", False)
            action = self.overlay.inventairedessin(self.ecran, self.joueur, pos, self.click, cliquedroit)
            if action and action[0] == "DROP":
                i = action[1]
                case = self.joueur.inventaire[i]
                titem = case["type"]
                if titem is not None:
                    case["quantite"]-=1
                    if titem=="piece":
                        self.joueur.pieces -= 1
                    elif titem == "munition":
                        self.joueur.munition -= 1
                    elif titem in "cristal":
                        self.joueur.cristal = False
                    if case["quantite"] <= 0:
                        case["type"] = None
                    px = self.joueur.rect.centerx+random.randint(-40,40)
                    py = self.joueur.rect.centery+random.randint(-40,40)
                    objsur = Objet(px, py, f"img_{titem}", titem, size=(40,40))
                    objsur.quantite = 1
                    self.objets.append(objsur)
        pygame.display.flip()
        return "CONTINUER"
    
def lancer(ecran, mode="solo", ip = None, save=None):
    partie = Partie(ecran, mode, ip, save)
    clock = pygame.time.Clock()
    running = True
    while running:
        partie.LARGEUR, partie.HAUTEUR = ecran.get_size()
        t = clock.tick(60) / 1000.0
        menuouv = (partie.enpause or getattr(partie,"moteurouvert", False) or getattr(partie,"boutiqueouverte", False) or getattr(partie,"ouvertemenu", False) or getattr(partie,"inventaire", False) or (hasattr(partie,"menusommeil") and partie.menusommeil.cours))
        pygame.mouse.set_visible(menuouv)
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