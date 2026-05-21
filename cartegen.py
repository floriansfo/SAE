import pygame
import random
import math
import assets
from prerequis import *
from prerequis import texture


class Objet:
    def __init__(self,x,y,name,type,size=None,cote=None):
        #Taille des texture
        if size:
            taillew,tailleh = size
        else:
            taillew,tailleh = ZOOM, ZOOM
        #Position et taille objet
        self.rect = pygame.Rect(0,0,taillew,tailleh)
        if cote == "bas":
            self.rect.centerx = x+ZOOM//2
            self.rect.bottom = y +ZOOM
        elif cote == "haut":
            self.rect.centerx = x+ZOOM//2
            self.rect.top = y
        elif cote == "droite":
            self.rect.right = x+ZOOM
            self.rect.centery = y +ZOOM//2
        elif cote == "gauche":
            self.rect.left = x
            self.rect.centery = y +ZOOM//2
        else:
            self.rect.x = x
            self.rect.y = y
        if not hasattr(Objet, 'texture_cache'):
            Objet.texture_cache = {}
        clecache = (name, size)
        #Si on redimensionne pas
        if clecache not in Objet.texture_cache:
            image= assets.ASSETS['img_deco'].get(name)
            if image is None:
                image = assets.ASSETS.get(name)
            if image is not None:
                #Redimensionner et sauvegarder
                Objet.texture_cache[clecache] = pygame.transform.scale(image, (taillew, tailleh))
            else:
                #Sinon on recharche et ca bouffe
                Objet.texture_cache[clecache] = texture(name,size,transparente=True)
        self.texture=Objet.texture_cache[clecache]
        self.type = type  
        #Reduction hitbox si c'est un meuble
        if type in ("meuble", "deco"):
            self.hitbox = self.rect.inflate(-taillew//4,-tailleh//4)
        else:
            self.hitbox = self.rect.copy()
        
    def draw(self,surface, camera_x, camera_y):
        #Affichage de l'objet
        fenetre_x = self.rect.x + camera_x
        fenetre_y = self.rect.y + camera_y
        #On dessine objet
        surface.blit(self.texture, (fenetre_x, fenetre_y))
        return fenetre_y+self.rect.height

def tango(grille, salles, poscristal = None):
    objet = [] #corps et cristal
    if not salles:
        return objet, None
    #On cherche le centre de la 1 salle
    centre = salles[0].center
    #On cherche la salle la plus loin calcul grace a pythagore en fonction de la distance la plus loin avec la 1ere
    salleloin = max(salles[1:], key = lambda s: (s.centerx-centre[0])**2+(s.centery-centre[1])**2)
    sx = salleloin.centerx*ZOOM
    sy = salleloin.centery*ZOOM
    #Apparition cristal
    if poscristal:
        #Objet corps
        corps = Objet(sx-ZOOM//2, sy-ZOOM//2, "corps.png", 'corps', size =(ZOOM,ZOOM))
        objet.append(corps)
        #Objet cristal
        cristal = Objet(sx+ZOOM//4, sy-ZOOM//4, "cristal.png", 'cristal', size=(ZOOM//2, ZOOM//2))
        objet.append(cristal)
        cristalpos = (sx+ZOOM//4, sy-ZOOM//4)
        return objet, cristalpos

def generer_objets(grille, salles, multi = 1.0, niveau=1):
    objets = []
    densité=(niveau)*0.07
    #Dictionnaire des types et probabilité d'affichage des objets
    types = [{'nom': 'img_caisse', 'type': 'meuble', 'proba': 0.2, 'taille':ZOOM//2 },
            {'nom': 'img_plante', 'type': 'plante', 'proba': 0.2, 'taille':ZOOM//2},
            {'nom': 'img_meuble', 'type': 'meuble', 'proba': 0.2, 'taille':ZOOM//2},
            {'nom': 'img_munition', 'type': 'munition', 'proba':0.1 , 'taille':ZOOM//2}, ]
    if niveau>=2:
        types.append({'nom':'rock1','type': 'deco', 'proba': 0.3+densité, 'taille':ZOOM })
        types.append({'nom':'Veins1','type': 'deco', 'proba': 0.3+densité, 'taille':ZOOM})
    if niveau>=3:
        types.append({'nom':'Eye_plant1','type': 'deco', 'proba': 0.3+densité, 'taille':ZOOM})
        types.append({'nom':'Eye_plant2','type': 'deco', 'proba': 0.3+densité,'taille':ZOOM})
        types.append({'nom':'Veins2','type': 'deco', 'proba': 0.3+densité,'taille':ZOOM})
    if niveau>=4:
        types.append({'nom':'Eye_plant3','type': 'deco', 'proba': 0.15+densité, 'taille':ZOOM })
        types.append({'nom':'rock2','type': 'deco', 'proba': 0.3+densité, 'taille':ZOOM})
        types.append({'nom':'Veins3','type': 'deco', 'proba': 0.3+densité, 'taille':ZOOM})
        types.append({'nom':'Jaws1','type': 'deco', 'proba': 0.15+densité, 'taille':ZOOM})
        types.append({'nom':'Fetus1','type': 'deco', 'proba': 0.15+densité, 'taille':ZOOM})
    if niveau >=5:
        types.append({'nom':'plant1','type': 'deco', 'proba': 0.15+densité,'taille':ZOOM})
        types.append({'nom':'Jaws2','type': 'deco', 'proba': 0.15+densité,'taille':ZOOM })
        types.append({'nom':'Jaws3','type': 'deco', 'proba': 0.3+densité,'taille':ZOOM })
        types.append({'nom':'Jaws4','type': 'deco', 'proba': 0.15 +densité,'taille':ZOOM})
        types.append({'nom':'Fetus2','type': 'deco', 'proba': 0.15+densité,'taille':ZOOM })
        types.append({'nom':'Oeuil','type': 'deco', 'proba': 0.15+densité,'taille':ZOOM })
    if niveau >=6:
        types.append({'nom':'Meat1','type': 'deco', 'proba': 0.15+densité,'taille':ZOOM })
        types.append({'nom':'Meat2','type': 'deco', 'proba': 0.15+densité,'taille':ZOOM })
        types.append({'nom':'Meat3','type': 'deco', 'proba': 0.15+densité,'taille':ZOOM })
        types.append({'nom':'Meat4','type': 'deco', 'proba': 0.15+densité,'taille':ZOOM })
        types.append({'nom':'bones','type': 'deco', 'proba': 0.15+densité,'taille':ZOOM })
        types.append({'nom':'plant2','type': '', 'proba': 0.15+densité,'taille':ZOOM })
    
    for salle in salles:
        for y in range(salle.top, salle.bottom):
            for x in range(salle.left, salle.right):
                #On place des objets que sur les sols
                if grille[y][x] == SOL or grille[y][x] == SOL_ROUGE :
                    #Detecte les cote du mur
                    cotes = []
                    if grille[y+1][x] == MUR:
                        cotes.append("bas")
                    if grille[y-1][x] == MUR:
                        cotes.append("haut")
                    if grille[y][x+1] == MUR:
                        cotes.append("droite")
                    if grille[y][x-1] == MUR:
                        cotes.append("gauche")
                    if cotes and random.random()<(0.2*multi):
                        #Objet au hasard
                        t = random.choice(types)
                        #Verifie proba d'apparition
                        if random.random() < t['proba']:
                            taillemun = (t['taille'], t['taille'])
                            cotebon = random.choice(cotes)
                            #Creation de l'objet
                            obj = Objet(x*ZOOM, y*ZOOM, t['nom'], t['type'], size=taillemun, cote=cotebon)
                            objets.append(obj)
    if salles:
        salledialogue = random.choice(salles)
        dx = random.randint(salledialogue.x+1, salledialogue.x+salledialogue.w-2)
        dy = random.randint(salledialogue.y+1, salledialogue.y+salledialogue.h-2)
        objets.append(Objet(dx*ZOOM, dy*ZOOM, "img_cassette", "dialogue"))
    return objets

#couloir verticale
def c_vertical(grille, y1,y2,x, niveau=1):
    for y in range(min(y1,y2),max(y1,y2)+1):
        if random.random()<niveau/6:
            grille[y][x]=SOL_ROUGE
        else:
            grille[y][x]=SOL

#couloir horizontal
def c_horizontal(grille, x1,x2,y, niveau=1):
    for x in range(min(x1,x2),max(x1,x2)+1):
        if random.random()<niveau/6:
            grille[y][x]=SOL_ROUGE
        else:
            grille[y][x]=SOL

#generation map
def generemap(niveau=1):
    #Carte rempli de vide
    grille = [[VIDE for i in range(LARGEURMAP)] for k in range(HAUTEURMAP)]
    salles=[]
    distance_min =7
    distance_max = 10#Dstance entre les salles
    #Generation salle
    for k in range(80): #Nombre de salles a essayer de generer
        #Taille aléatoire
        w = random.randint(5,9)   
        h = random.randint(5,9)
        #Toute premiere salle au centre
        if not salles:
            x = LARGEURMAP//2 - w//2
            y = HAUTEURMAP//2 - h//2
            suivant = False
        else:
            #Pour les autres salles on part de celle qui existe
            suivant = random.choice(salles)
            place = False
            #On essaie 10 fois de trouver un espace autour de cette salle
            for i in range(10):
                angle = random.uniform(0, 2*math.pi)
                distance = random.randint(distance_min, distance_max)
                #Nouvelle coordonnée
                kx = int(suivant.centerx+ math.cos(angle)*distance) - (w//2)
                ky = int(suivant.centery + math.sin(angle)*distance) - (h//2)
                #Qu'on ne sort pas de la carte
                if 2<kx<LARGEURMAP-w-2 and 2<ky<HAUTEURMAP-h-2:
                    nouvelle_salle = pygame.Rect(kx,ky,w,h)
                    #Laisse 1 ecart de vide entre les salles
                    if not any(nouvelle_salle.inflate(2,2).colliderect(s) for s in salles):
                        x,y = kx, ky
                        place = True
            #Sinon on l'a crée pas
            if not place:
                continue
        #Creation et sauvegarde de salle
        nouvelle_salle = pygame.Rect(x,y,w,h)
        salles.append(nouvelle_salle)
        #Creuse le sol pour connecter
        for k in range(nouvelle_salle.top, nouvelle_salle.bottom):
            for v in range(nouvelle_salle.left, nouvelle_salle.right):
                #15% de mettre une racine
                if random.random() < 0.05:
                    grille[k][v] = RACINE
                elif random.random()< niveau/6:
                    grille[k][v] = SOL_ROUGE
                else:
                    grille[k][v] = SOL
        #Connecte les salle par couloir
        if suivant:
            #On creuse couloir jusqu'a la salle precedente
            prec = suivant.center
            proc = nouvelle_salle.center
            x1, y1 = int(prec[0]), int(prec[1])
            x2, y2 = int(proc[0]), int(proc[1])
            #On choisis alétoirement si vertical ou pas
            if random.choice([True, False]):
                c_horizontal(grille, x1, x2, y1, niveau)
                c_vertical(grille, y1, y2, x2, niveau)
            else:
                c_vertical(grille, y1, y2, x1, niveau)
                c_horizontal(grille, x1, x2, y2, niveau)
    
    #Placement du point de depart de l'ascnecer
    salle_depart = salles[0]
    px,py = int(salle_depart.centerx), int(salle_depart.centery)
    grille[py][px] = ASCENCEUR
    
    #On fait copir de la grille pour cree mur
    grille_fin = [row[:] for row in grille]
    for y in range(1, HAUTEURMAP-1):
        for x in range(1, LARGEURMAP-1):
            if grille[y][x]==VIDE:
                #On regarde si case vide touche un sol alors devient MUR
                voisin = False
                if grille[y+1][x] in (SOL,SOL_ROUGE) or grille[y-1][x]in (SOL, SOL_ROUGE) or grille[y][x+1]in (SOL, SOL_ROUGE) or grille[y][x-1]in (SOL, SOL_ROUGE):
                    grille_fin[y][x] = MUR
    return grille_fin, salles, salles[0].center