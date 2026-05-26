import json
import os
from datetime import datetime
from prerequis import texture






def fichier_slot(slot):
    return f"sauvegarde_{slot}.json"




def sauvegarder(partie, niveau_actuel, modifs_etage, joueur, slot=1):  # collecte les données et les sauvegarde dans un fichier json
    data = {
        "seed": partie,
        "niveau_actuel": niveau_actuel,
        
        "date": datetime.now().strftime("%d/%m/%Y %H:%M"), #timestamp de la sauvegarde
        
        "joueur": {
            "x": joueur.rect.centerx,
            "y": joueur.rect.centery,
            "hp": joueur.hp,
            "hpmax": joueur.hpmax,
            "munition": joueur.munition,
            "arsenal": joueur.arsenal,
            "arsenal_achete": joueur.arsenal_achete,
            "endurance": joueur.endurance,
            "pieces": joueur.pieces,
            "malachite": joueur.malachite,
            "possedelampe": joueur.possedelampe,
            "pile": joueur.pile,
            "inventaire": joueur.inventaire,
            "cristal": joueur.cristal, 
            "niveaudebloque": list(joueur.niveaudebloque), # conversion into list pour passer dans le json
        },
    }
    modifs_str = {}
    for k, v in modifs_etage.items(): # clés to str pour save dans le json
        modifs_str[str(k)] = v
    data["modifs"] = modifs_str
    
    
    f = open(fichier_slot(slot), "w")
    json.dump(data, f, indent=2) # indent=2 pour ajouter des espaces pour la lisibilité
    f.close()
    print(f"Partie sauvegardée dans le slot {slot}.")

def charger(slot=1):
    try:
        f = open(fichier_slot(slot), "r")
        data = json.load(f)
        f.close()
        return data
    except FileNotFoundError:
        return None

def charger_tous():
    # Retourne une liste de 3 éléments : la save de chaque slot ou None
    return [charger(slot) for slot in range(1, 4)]





def appliquer_modifs(objets, modifs):
    if not modifs:
        return objets
    objetsreste = []
    for obj in objets:
        key = f"{obj.rect.x}-{obj.rect.y}"
        if key in modifs:
            if modifs[key] == "S":
                continue
            if modifs[key] == "M":
                obj.type = "munition"
                obj.texture = texture("munition.png", (90, 90), transparente=True)
                obj.hitbox = obj.rect
        objetsreste.append(obj)
    return objetsreste
