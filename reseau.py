import pygame
import assets
from joueur import Joueur

def connexion(socket_jeu, joueur, monstres, objets, actionmap, mort, niveau_actuel, buffer, joueursup):
    #Reseaux
    #position balle
    balle = "vide"
    if len(joueur.tir) > 0:
        balle = "_".join([f"{int(b.rect.x)}={int(b.rect.y)}={b.ux:.2f}={b.uy:.2f}={getattr(b, 'id',1)}" for b in joueur.tir])
    #Modification de la map sauvegarde
    modifmap = "vide"
    if len(actionmap) > 0:
        modifmap = "_".join([f"{coordonne}={etat}" for coordonne, etat in actionmap.items()])
        actionmap.clear() #Vide liste
    monstree = "vide"
    if len(monstres)>0:
        monstree = "_".join([f"{int(m.rect.x)}={int(m.rect.y)}={int(m.mort)}" for m in monstres])
    objetsol = "vide"
    if hasattr(joueur, 'objetsol') and len(joueur.objetsol) > 0:
        objetsol = "_".join([f"{o['type']}={o['quantite']}={o['x']}={o['y']}={o['etage']}" for o in joueur.objetsol])
        joueur.objetsol.clear()
    try:
        #Mort ou pas
        if mort:
            etatmort = 1
        else:
            etatmort = 0
        lumiere = 1 if getattr(joueur, "lumiereallumee", False) else 0
        dsvaisseau = 1 if getattr(joueur, "dsvaisseau", False) else 0
        #Envoie la position du joueur
        angleactuel = getattr(joueur, "angleactuel", joueur.angle)
        message = f"{joueur.rect.centerx},{joueur.rect.centery},{niveau_actuel},{joueur.angle},{joueur.animation},{balle},{modifmap},{etatmort},{monstree},{lumiere},{angleactuel},{objetsol},{dsvaisseau}\n"
        socket_jeu.send(message.encode('utf-8'))
        data = socket_jeu.recv(4096)
        if data:
            buffer += data
            if b"\n" in buffer:
                paquet, buffer = buffer.split(b"\n", 1)
                paquetss = paquet.decode('utf-8').split('|')
                if len(paquetss) > 1:
                    #On traite les anciens
                    for paquet in paquetss[:-1]:
                        if not paquet:
                            continue
                        if ';'not in paquet:
                            continue
                        idjoueur, reste = paquet.split(';', 1)
                        v = reste.split(',')
                        if len(v)<10:
                            continue
                        if idjoueur not in joueursup:
                            joueursup[idjoueur] = Joueur(int(v[0]), int(v[1]))
                        autre = joueursup[idjoueur]
                        autre = joueursup[idjoueur]
                        autre.rect.centerx = int(v[0])
                        autre.rect.centery = int(v[1])
                        autre.etage = int(v[2])
                        autre.angle = float(v[3])
                        autre.animation = int(v[4])
                        autre.mort = bool(int(v[7]))
                        autre.lumiere = bool(int(v[9]))
                        if len(v)>10:
                            autre.angleactuel = float(v[10])
                        if len(v)>11 and v[11] != "vide":
                            if not hasattr(joueur, 'objsol'):
                                joueur.objsol = []
                            for obj in v[11].split('_'):
                                parts = obj.split('=')
                                if len(parts)==5:
                                    joueur.objsol.append({'type': parts[0], 'quantite': int(parts[1]), 'x': int(parts[2]), 'y': int(parts[3]), 'etage': int(parts[4])})
                        if len(v)>12:
                            autre.dsvaisseau = bool(int(v[12]))
                        #Balles
                        if v[6] != "vide":
                            for m in v[6].split('_'):
                                p = m.split('=')
                                if len(p)==2:
                                    coordonne, etat = p
                                    if coordonne== "REVIVE" and etat == "GO":
                                        joueur.hp = joueur.hpmax
                                    else:
                                        try:            
                                            mx, my = map(int, coordonne.split('-'))
                                            if etat == "S":
                                                objets = [o for o in objets if not (o.rect.x == mx and o.rect.y == my)]
                                            elif etat == "M":
                                                for o in objets:
                                                    if o.rect.x == mx and o.rect.y == my:
                                                        o.type = "munition"
                                                        o.texture = assets.ASSETS.get('img_munition', o.texture)
                                        except ValueError:
                                            pass
                        autre.balles_reseau = []
                        if v[5] != "vide":
                            for b in v[5].split('_'):
                                parti = b.split('=')
                                if len(parti)==5:
                                    ballex,balley,balledx,balledy,balleid = parti
                                    autre.balles_reseau.append((int(ballex), int(balley),float(balledx),float(balledy), int(balleid)))
                        #Monstres
                        autre.monstres_reseau = []
                        if v[8] != "vide":
                            for m in v[8].split('_'):
                                parts = m.split('=')
                                if len(parts)==3:
                                    mx,my,mmort = parts
                                    autre.monstres_reseau.append((int(mx),int(my), int(mmort)))
    except BlockingIOError: pass
    except Exception: pass
    return buffer, objets, joueursup