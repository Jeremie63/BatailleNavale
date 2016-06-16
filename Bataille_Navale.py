# dataGrid représente un tableau de données, chaque case est un char
class dataGrid:
    def __init__(self,tailleX,tailleY,ID):
        self.ID = ID
        self.tailleX = tailleX
        self.tailleY = tailleY    
    # on crée le tableau
        self.grid = [["0" for x in range(tailleX)] for x in range(tailleY)]
        
    # retourne la valeur contenu à la case x,y si "0" retourne 0 
    def getDataID(self,x,y):
        if self.grid[y][x] != "0":
            return self.grid[y][x]
        else:
            return 0
    
    # met à jour la grille, utile seulement après le placement de bateau
    def update(self,side):
        for ba in bateau.toutBateau:
                if ba.side == side:
                    self.conversionBateauData(ba)
    
    # change directement le contenu d'une case
    def changementData(self,x,y,data):
        self.grid[y][x] = data
        
    # transforme un objet bateau en data à placer dans la grille  
    def conversionBateauData(self,bateau):
        for pos in bateau.pos:
            self.grid[pos[1]][pos[0]] = bateau.ID
            
    # compte le nombre de T (correspond à une partie touchée)
    # si cette valeur dépasse le total de toutes les parties des bateaux, 
    # alors le joueur a perdu
    def compteurBateauxDetruits(self,looseValue):
        result = False
        detruit = 0
        for y in self.grid:
            for obj in y:
                if obj == "T":
                    detruit += 1
        if detruit == looseValue:
            result = True
        return result
    
    # affiche la grille 
    def afficherGrille(self):
        temp = ""
        print("-------------------------------------------")
        print("  | A | B | C | D | E | F | G | H | I | J |")
        for ix,y in enumerate(self.grid):
            temp = ""
            print("-------------------------------------------")
            for x in y:
                temp +=  str(x) + " | "
                
            if ix > 8:
                temp = str(ix+1)+ "| " + temp
            else:
                temp = str(ix+1)+ " | " + temp
            print(temp)
        print("-------------------------------------------")

class bateau:
    toutBateau = []
    lastID = 0
    def __init__(self,y,x,orientation,taille,camp):
        self.pos = []
        self.taille = taille
        self.ID = bateau.lastID + 1
        bateau.lastID += 1
        self.deltaX = 0
        self.deltaY = 0
        self.orientation = orientation
        self.x = x
        self.y = y
        self.side = camp
        
        # peut être optimisé en utilisant le prebuild
        # 1 = bas, 2 = droite, 3 = haut, 4 = gauche, 0 = rien (bateau 1 case)
        if self.orientation == 1:
            self.deltaY = 1
        if self.orientation == 2:
            self.deltaX = 1
        if self.orientation == 3:
            self.deltaY = -1
        if self.orientation == 4:
            self.deltaX = -1
        
        self.pos.append([x,y])
        for i in range(1,taille):
            self.pos.append([self.x + self.deltaX, self.y + self.deltaY]) 
            self.x += self.deltaX
            self.y += self.deltaY
        
        bateau.toutBateau.append(self)
                    
# test si un navire n'est pas en collision avec un autre sur la grille          
def collision(pos,side,ID):
    result = False
    for bateauCombat in bateau.toutBateau:
        for i in range(0,bateauCombat.taille-1):
            for position in pos:
                if bateauCombat.pos[i] == position and bateauCombat.ID != ID and bateauCombat.side == side:
                    result = True
    return result

# crée un prebuild (version "simulée" d'un navire)
# pour permettre d'effectuer les vérifications de position
def prebuild(py,px,orientation,taille):
    pos = []
    x = px
    y = py
    deltaX = 0
    deltaY = 0
    
    # les delta permettent d'incrémenter les positions lors de la création
    # de la liste de positions.
    if orientation == 1:
        deltaY = 1
    elif orientation == 2:
        deltaX = 1
    elif orientation == 3:
        deltaY = -1
    elif orientation == 4:
        deltaX = -1
    
    # création de la liste de positions du bateau
    pos.append([x,y])
    for i in range(1,taille):
        pos.append([x + deltaX, y + deltaY]) 
        x += deltaX
        y += deltaY
    return pos                 
      
# test si le bateau est en dehors de la grille
def horsJeu(pos,orientation,taille):
    result = False
    if orientation == 1 and pos[0] + taille > 10:
        result = True
    elif orientation == 2 and pos[1] + taille > 10:
        result = True
    elif orientation == 3 and pos[0] - taille < 0:
        result = True
    elif orientation == 4 and pos[1] - taille < 0:
        result = True
    return result


aucunGagnant = True

# dictionnaire de conversion des coordonnées rentrées avec les coordonnées réelles
converter = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9,"1":0,"2":1,"3":2,"4":3,"5":4,"6":5,"7":6,"8":7,"9":8,"10":9,"HAUT":3,"BAS":1,"DROITE":2,"GAUCHE":4 };

# fonction pour placer un bateau avec vérification de position: 
# créer d'abord un prebuild du navire et vérifie qu'il ne risque
# pas de dépasser ou de rentrer dans un autre bateau
def placerBateau(camp,taille,description):
    set = False
    pre = []
    bat = 0
    orientation = 0
    
    while set == False:
        print(description)
        pos = input("Entrez la position du bateau sous la forme: 1 A (ligne colonne): ").split(' ')
        pos[0] = converter[pos[0]]
        pos[1] = converter[pos[1]]
        if taille > 1:
            orientation = converter[input("Orientation bas/haut/droite/gauche ? ").upper()]        
        pre = prebuild(int(pos[0]), int(pos[1]), orientation, taille)
        if collision(pre, camp, 0) == False and horsJeu(pos,orientation,taille) == False:
            set = True
        else:
            print("Erreur: mauvais placement, un navire sors de la carte ou est en collision avec un autre. ")
    bat = bateau(pos[0],pos[1],orientation,taille,camp)
    
# effectue un tir avec vérification d'erreur de position
def tirer(p1,p2,p1_tirer,p2_tirer,originCamp):
    result = False
    pos = input("Coordonnées du tir ? ").split(' ')
    pos[0] = converter[pos[0]]
    pos[1] = converter[pos[1]]
    x = pos[1]
    y = pos[0]
    
    while (x < 0 or x > 10) or (y < 0 or y > 10):
        pos = input("Erreur ! Coordonnées du tir ? ").split(' ')
        pos[0] = converter[pos[0]]
        pos[1] = converter[pos[1]]
        x = pos[1]
        y = pos[0]
    
    if originCamp == 1:
        if p2.getDataID(x,y) != 0:
            print("Touché !")
            p2.changementData(x,y,"T")
            p1_tirer.changementData(x,y,"T")
            result = True
        else:
            print("Raté !")
            p1_tirer.changementData(x,y,"x")
            
    elif originCamp == 2:
        if p1.getDataID(x,y) != 0:
            print("Touché !")
            p1.changementData(x,y,"T")
            p2_tirer.changementData(x,y,"T")
            result = True
        else:
            print("Raté !")
            p2_tirer.changementData(x,y,"x")
    return result


clear = "\n" * 100
temp = ""

gagnant = 0

P1 = dataGrid(10,10,1)
p1_tirer = dataGrid(10,10,1)
P2 = dataGrid(10,10,2)
p2_tirer = dataGrid(10,10,2)


input("C'est au tour du joueur 1 de placer ses bateaux, appuyez sur entrée. ")
placerBateau(1, 5, "Porte-avions: 5 cases")
P1.update(1)
P1.afficherGrille()
placerBateau(1, 4, "Croiseur: 4 cases")
P1.update(1)
P1.afficherGrille()
placerBateau(1, 3, "Destroyer: 3 cases")
P1.update(1)
P1.afficherGrille()
placerBateau(1, 3, "Sous-marin: 3 cases")
P1.update(1)
P1.afficherGrille()
placerBateau(1, 2, "Torpilleur: 2 cases")
P1.update(1)
P1.afficherGrille()

input("Appuyez sur entrée pour laisser la place au joueur 2. ")
print(clear)

input("C'est au tour du joueur 2 de placer ses bateaux, appuyez sur entrée. ")
placerBateau(2, 5, "Porte-avions: 5 cases")
P2.update(2)
P2.afficherGrille()
placerBateau(2, 4, "Croiseur: 4 cases")
P2.update(2)
P2.afficherGrille()
placerBateau(2, 3, "Destroyer: 3 cases")
P2.update(2)
P2.afficherGrille()
placerBateau(2, 3, "Sous-marin: 3 cases")
P2.update(2)
P2.afficherGrille()
placerBateau(2, 2, "Torpilleur: 2 cases")
P2.update(2)
P2.afficherGrille()

input("Les navires sont bien placés, place au jeu, appuyez sur entrée ! ")
print(clear)


while aucunGagnant:  
    input("Joueur 1, appuyez sur entrée. ")
    print("Votre carte: ")
    P1.afficherGrille()
    print("\n vos tirs: ")
    p1_tirer.afficherGrille()
    
    while tirer(P1, P2, p1_tirer, p2_tirer, 1) and P2.compteurBateauxDetruits(15) == False:
        print("\n vos tirs: ")
        p1_tirer.afficherGrille()
        
    input("Joueur 2, appuyez sur entrée. ")
    print(clear)
    print("Votre carte: ")
    P2.afficherGrille()
    print("\n vos tirs: ")
    p2_tirer.afficherGrille()
    
    while tirer(P1, P2, p1_tirer, p2_tirer, 2) and P1.compteurBateauxDetruits(15) == False:
        print("\n vos tirs: ")
        p2_tirer.afficherGrille()
        
    print(clear)
    
    if P2.compteurBateauxDetruits(15):
        print("Le joueur 2 a perdu ! ")
        aucunGagnant = False
    if P1.compteurBateauxDetruits(15):
        print("Le joueur 1 a perdu ! ")
        aucunGagnant = False
