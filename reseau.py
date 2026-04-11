import pygame
import assets
from joueur import Joueur

def connexion(socket_jeu, joueur, monstres, objets, actionmap, mort, niveau_actuel, buffer, joueursup):
    #Reseaux
    #position balle
    balle = "vide"
    if len(joueur.tir) > 0:
        balle = "_".join([f"{int(b.rect.x)}={int(b.rect.y)}={b.dx:.2f}={b.dy:.2f}" for b in joueur.tir])
    #Modification de la map sauvegarde
    modifmap = "vide"
    if len(actionmap) > 0:
        modifmap = "_".join([f"{coordonne}={etat}" for coordonne, etat in actionmap.items()])
        actionmap.clear() #Vide liste
    monstree = "vide"
    if len(monstres)>0:
        monstree = "_".join([f"{int(m.rect.x)}={int(m.rect.y)}={int(m.mort)}" for m in monstres])
    try:
        #Mort ou pas
        if mort:
            etatmort = 1
        else:
            etatmort = 0
        #Envoie la position du joueur
        message = f"{joueur.rect.centerx},{joueur.rect.centery},{niveau_actuel},{joueur.angle},{joueur.animation},{balle},{modifmap},{etatmort},{monstree}\n"
        socket_jeu.send(message.encode('utf-8'))
    except BlockingIOError: pass
    except Exception as e: pass
    #Reçoit la position de l'autre joueur
    try:
        data = socket_jeu.recv(4096)
        if data:
            buffer += data
            if b"\n" in buffer:
                texte = buffer.decode('utf-8')
                paquetss = texte.split("\n")
                dernier = paquetss[-2] #Isole dernier paquet
                try:
                    #On traite les anciens
                    for paquet in paquetss[:-1]:
                        if paquet:
                            listejoueur = paquet.split('|')
                            for j in listejoueur:
                                if j:
                                    jid, jinfos = j.split(':', 1)
                                    v = jinfos.split(',')
                                    #Si modif de carte
                                    if len(v)>=7 and v[6] != "vide":
                                        for m in v[6].split('_'):
                                            coordonne, etat = m.split('=')
                                            mx, my = coordonne.split('-')
                                            mx, my = int(mx), int(my)
                                            #Maintenant on ajoute la modif sur notre map
                                            objsup = None
                                            for obj in objets:
                                                if obj.rect.x == mx and obj.rect.y == my:
                                                    if etat == "S":
                                                        objsup = obj
                                                    elif etat == "M" and getattr(obj, "type", "") != "munition":
                                                        #Caisse devient mun
                                                        obj.type = "munition"
                                                        obj.texture = assets.ASSETS['img_munition']
                                                        obj.hitbox = obj.rect
                                            #Objet ramassé
                                            if objsup in objets:
                                                objets.remove(objsup)
                    #Met a jour pos des joueur
                    if dernier:
                        listejoueur = dernier.split('|')
                        for j in listejoueur:
                                if j:
                                    jid, jinfos = j.split(':', 1)
                                    v = jinfos.split(',')
                                    if len(v) >= 9:
                                        #Si nouveau joueur on l'ajoute au dico
                                        if jid not in joueursup:
                                            joueursup[jid] = Joueur(int(v[0]), int(v[1]))
                                        #Met a jour stat
                                        autre = joueursup[jid]
                                        autre.rect.centerx = int(v[0])
                                        autre.rect.centery = int(v[1])
                                        autre.etage = int(v[2])
                                        autre.angle = float(v[3])
                                        autre.animation = int(v[4])
                                        autre.mort = bool(int(v[7]))
                                        #Lecture des balles
                                        autre.balles_reseau = []
                                        if v[5] != "vide":
                                            for b in v[5].split('_'):
                                                parti = b.split('=')
                                                if len(parti)==4:
                                                    ballex,balley,balledx,balledy = parti
                                                    autre.balles_reseau.append((int(ballex), int(balley),float(balledx),float(balledy)))
                                        #Monstres
                                        autre.monstres_reseau = []
                                        if v[8] != "vide":
                                            for m in v[8].split('_'):
                                                parts = m.split('=')
                                                if len(parts)==3:
                                                    mx,my,mmort = parts
                                                    autre.monstres_reseau.append((int(mx),int(my), int(mmort)))
                except Exception as e:
                    pass
                buffer = paquetss[-1].encode('utf-8')
    except BlockingIOError: pass
    except Exception: pass
    return buffer, objets, joueursup