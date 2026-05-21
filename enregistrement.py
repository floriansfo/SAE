import pygame
import assets

DIALOGUE = {
    0: "Enregistrement n°7 : Captain Sierra\n *grzt* *crachat* Ils sont tous… *grzt* de la vie… *grzt* … hostile *grzt* en bas *grzt* source…",
    1: "Enregistrement n°1 : Soldier Mike\n *grzt* *tape* Soldier Mike, 16 juillet 3001. L’exploration de D-RED est très fructueuse. On détecte une immense quantité d’énergie enfouie profondément sous terre. On soupçonne qu’une espèce intelligente ait construit ses souterrains pour l’exploiter… Echo, qu’est-ce que tu fous ? Je vais pas t’abandonner, pas besoin de me coller ! Bref, nous continuons vers les profondeurs, mais une espèce étrange semble avoir envahi *cri* *grzt*",
    2: "Enregistrement n°2 : Soldier Echo\n *grzt* Soldier Echo, 17… roh et puis merde. Ces chiens m’ont rétrogradé ! Ce salaud de Mike s’est barré sans moi, mais bien sûr c’est moi qui prends. Et puis, qui a été nommé capitaine ? Ce merdeux de Sierra, le plus lâche évidemment ! *rugissement* C’était quoi ça ? Merde, c’est qu’on voit rien ici… Merde, merde, merde ! *grzt*",
    3: "Enregistrement n°3 : Soldier Victor\n *grzt* Soldier Victor, 18 juillet 3001. Nous avons perdu deux membres de l’équipe dans les niveaux supérieurs. Il semblerait qu’Echo ait ramené quelque chose de sa mission précédente, qui a pris possession du cadavre de Mike. Il ne faut surtout pas que cette espèce atteigne *asphyxie* *grzt*",
    4: "Enregistrement n°4 : Soldier Papa\n *grzt* Soldier Papa, 19 juillet 3001. Nous sommes sur le point de rencontrer une espèce de vie intelligente ayant habité D-RED, nous entendons des enfants ! Quelle révolution, la Terre apprendra aujourd’hui que nous ne sommes pas seuls !",
    5: "Enregistrement n°5 : Soldier November\n *grzt* Soldier November, 20 juillet 3001. Après l’attaque contre Papa hier, nous avons finalement décidé d’appeler du renfort. Le parasite a progressé, et on soupçonne qu’il ait profité des complexes de ventilation pour s’enfoncer en toute discrétion jusqu’à notre destination. Nous ne pouvons plus reculer. […] Merde, elle déconne… Je vois rien… Je me sens si… *grzt.*",
    6: "Enregistrement n°6 : Soldier Tango\n *grzt* Soldier Tango, 21 juillet 3001. Tout est perdu. Le parasite a atteint le réacteur du niveau -10, le plus puissant que nous ayons trouvé pendant toutes nos explorations sur n’importe quelle planète, et a par je-ne-sais quel miracle converti l’énergie thermique en énergie vitale, et s’est développé en un individu immortel qui traque tout l’équipage. Nous ne sommes plus que deux. Chérie, je t’aime. Je t’aime très fort. *grzt*",
}

class Enregistrement:
    def __init__(self, largeur, hauteur):
        self.titre = pygame.font.Font("ressource/fonts/polices.ttf", 25)
        self.texte = pygame.font.Font("ressource/fonts/polices.ttf", 20)
        self.ouvert = False
        self.dialogue = 0
        self.texteentier = ""
        self.index = 0
        self.vitesse = 1.5
        self.enregistrement = pygame.mixer.Channel(5)

    def ouvrir(self, niveau):
        self.dialogue = niveau
        self.texteentier = DIALOGUE.get(self.dialogue, DIALOGUE[0])
        self.index = 0
        self.ouvert = True
        self.son = assets.ASSETS.get('voix', {}).get(self.dialogue)
        if self.son:
            self.enregistrement.play(self.son)

    def fermer(self):
        self.ouvert = False
        self.enregistrement.stop()
    
    def affichage(self, surface, texte, couleur, rect, police):
        y = rect.y
        par = texte.split('\n')
        dernierx = rect.x
        derniery = y
        for p in par:
            mot = p.split(' ')
            ligne = []
            ligneactuelle = []
            for m in mot:
                ligneactuelle.append(m)
                larg, _ = police.size(' '.join(ligneactuelle))
                if larg > rect.width:
                    ligneactuelle.pop()
                    ligne.append(' '.join(ligneactuelle))
                    ligneactuelle = [m]
            ligne.append(' '.join(ligneactuelle))
            for l in ligne:
                surface.blit(police.render(l, True, couleur), (rect.x, y))
                dernierx = rect.x + police.render(l, True, couleur).get_width()
                derniery = y
                y += police.get_height() + 5
            y+= 15
        return dernierx, derniery
    
    def dessiner(self, ecran):
        if not self.ouvert:
            return
        resl, resh = ecran.get_size()
        marge = 50
        hauteurtexte = 250
        self.fondrect = pygame.Rect(marge, resh-hauteurtexte-marge,resl-(marge*2), hauteurtexte)
        #Fond semi-transparent
        fond = pygame.Surface((resl, resh), pygame.SRCALPHA)
        fond.fill((0,0,0,200))
        ecran.blit(fond, (0,0))
        #Dialogue
        pygame.draw.rect(ecran, (10,15,10), self.fondrect, border_radius=10)
        pygame.draw.rect(ecran, (50,220,50), self.fondrect, 3, border_radius=10)
        #Titre
        titre = self.titre.render(f"Lecture audio {self.dialogue}...", True, (100,255,100))
        ecran.blit(titre, (self.fondrect.x+20, self.fondrect.y + 20))
        #Effet ecrire 
        if self.index < len(self.texteentier):
            self.index += self.vitesse
        #Coupe au nombre qui rentre sur la ligne
        affiche = self.texteentier[:int(self.index)]
        #Affichage
        recttexte = pygame.Rect(self.fondrect.x+20, self.fondrect.y + 70, self.fondrect.width - 40, self.fondrect.height - 100)
        #Couleur verte
        finx, finy = self.affichage(ecran, affiche, (100,255,100), recttexte, self.texte)
        #Curseur 
        if pygame.time.get_ticks()%1000<500: #Clignote toyt les 500ms
            curseur = self.texte.render("_", True, (100,255,100))
            ecran.blit(curseur, (finx+20, finy))
        #Fermer
        if self.index>=len(self.texteentier):
            txtferme = self.texte.render("Appuyez sur ECHAP pour fermer", True, (50,150,50))
            ecran.blit(txtferme, txtferme.get_rect(bottomright =(self.fondrect.right-20, self.fondrect.bottom-15)))