import random
import numpy as np


def creer_salle():
    largeur = random.randint(4, 10)
    hauteur = random.randint(4, 10)
    x = random.randint(0, 40 - largeur)
    y = random.randint(0, 40 - hauteur)

    salle = {
        "x": x,
        "y": y,
        "largeur": largeur,
        "hauteur": hauteur
    }
    return salle


def chevauchement(salle1, salle2)-> bool:
    if(salle1["x"] + salle1["largeur"] <= salle2["x"]):
        return False
    elif(salle1["y"] + salle1["hauteur"] <= salle2["y"]):
        return False
    elif(salle2["y"] + salle2["hauteur"] <= salle1["y"]):
        return False
    elif(salle2["x"] + salle2["largeur"] <= salle1["x"]):
        return False
    else:
        return True


#salle1 = {
#    "x": 15,
#    "y": 14,
#    "largeur": 5,
#    "hauteur": 4
#}
#salle2 = {
#    "x": 5,
#    "y": 4,
#    "largeur": 4,
#    "hauteur": 3
#}
#print(chevauchement(salle1, salle2))


def generer_salles():
    salles = []

    for i in range(8):
        placee = False
        essais = 0
        while not placee and essais < 100:
            nouvelle_salle = creer_salle()
            valide = True
            for salle in salles:
                if chevauchement(nouvelle_salle, salle):
                    valide = False
                    break
            if valide:
                salles.append(nouvelle_salle)
                placee = True
            essais += 1
        if not placee:
            return None

    return salles


#salles = generer_salles()
#if salles is not None:
#    for salle in salles:
#        print(salle)
#else:
#    print("Impossible de placer toutes les salles.")


def creer_couloir(salle1, salle2):
    x1 = salle1["x"] + salle1["largeur"] // 2
    y1 = salle1["y"] + salle1["hauteur"] // 2
    x2 = salle2["x"] + salle2["largeur"] // 2
    y2 = salle2["y"] + salle2["hauteur"] // 2
    couloir = [(x1, y1)]

    while x1 != x2:
        if x1 < x2:
            x1 += 1
        else:
            x1 -= 1
        couloir.append((x1, y1))
    while y1 != y2:
        if y1 < y2:
            y1 += 1
        else:
            y1 -= 1
        couloir.append((x1, y1))

    return couloir


#salle1 = {
#    "x": 2,
#    "y": 2,
#    "largeur": 5,
#    "hauteur": 4
#}
#salle2 = {
#    "x": 15,
#    "y": 10,
#    "largeur": 6,
#    "hauteur": 5
#}
#print(creer_couloir(salle1, salle2))


def generer_couloirs(salles, graphe):
    couloirs = []

    for salle in graphe:
        for voisine in graphe[salle]:
            if salle < voisine:
                couloir = creer_couloir(salles[salle], salles[voisine])
                couloirs.append(couloir)

    return couloirs


#salles = generer_salles()
#couloirs = generer_couloirs(salles)
#print("Nombre de salles :", len(salles))
#print("Nombre de couloirs :", len(couloirs))


def creer_carte(salles, couloirs):
    carte = []

    for y in range(40):
        ligne = []
        for x in range(40):
            ligne.append(" ")
        carte.append(ligne)
    for salle in salles:
        for y in range(salle["y"], salle["y"] + salle["hauteur"]):
            for x in range(salle["x"], salle["x"] + salle["largeur"]):
                carte[y][x] = "S"
    for couloir in couloirs:
        for x, y in couloir:
            if carte[y][x] == " ":
                carte[y][x] = "."

    return carte


def afficher_carte(carte):
    print("+" + "-" * 40 + "+")
    for ligne in carte:
        print("|" + "".join(ligne) + "|")
    print("+" + "-" * 40 + "+")



#salles = generer_salles()
#couloirs = generer_couloirs(salles)
#carte = creer_carte(salles, couloirs)
#afficher_carte(carte)


def creer_graphe(salles):
    graphe = {}

    for i in range(len(salles)):
        graphe[i] = []
    for i in range(len(salles) - 1):
        graphe[i].append(i + 1)
        graphe[i + 1].append(i)

    return graphe


#salles = generer_salles()
#graphe = creer_graphe(salles)
#print(graphe)


def creer_matrice_adjacence(graphe):
    nombre_salles = len(graphe)
    matrice = []

    for i in range(nombre_salles):
        ligne = []
        for j in range(nombre_salles):
            ligne.append(0)
        matrice.append(ligne)
    for salle in graphe:
        for voisine in graphe[salle]:
            matrice[salle][voisine] = 1

    return matrice


def creer_matrice_laplacienne(matrice):
    nombre_salles = len(matrice)
    laplacienne = []

    for i in range(nombre_salles):
        ligne = []
        degre = 0
        for j in range(nombre_salles):
            degre += matrice[i][j]
        for j in range(nombre_salles):
            if i == j:
                ligne.append(degre - matrice[i][j])
            else:
                ligne.append(-matrice[i][j])
        laplacienne.append(ligne)

    return laplacienne


#salles = generer_salles()
#graphe = creer_graphe(salles)
#matrice = creer_matrice_adjacence(graphe)
#laplacienne = creer_matrice_laplacienne(matrice)
#print("Matrice d'adjacence :")
#for ligne in matrice:
#    print(ligne)
#print("Matrice laplacienne :")
#for ligne in laplacienne:
#    print(ligne)


def calculer_rang(matrice, tolerance=1e-10):
    nombre_lignes = len(matrice)
    nombre_colonnes = len(matrice[0])
    resultat = []

    for ligne in matrice:
        resultat.append([float(valeur) for valeur in ligne])
    
    rang = 0

    for colonne in range(nombre_colonnes):
        pivot = rang
        for i in range(rang, nombre_lignes):
            if abs(resultat[i][colonne]) > abs(resultat[pivot][colonne]):
                pivot = i
        if abs(resultat[pivot][colonne]) <= tolerance:
            continue
        resultat[rang], resultat[pivot] = resultat[pivot], resultat[rang]
        for i in range(rang + 1, nombre_lignes):
            facteur = resultat[i][colonne] / resultat[rang][colonne]
            for j in range(colonne, nombre_colonnes):
                resultat[i][j] -= facteur * resultat[rang][j]
        rang += 1
        if rang == nombre_lignes:
            break

    return rang


#salles = generer_salles()
#graphe = creer_graphe(salles)
#matrice = creer_matrice_adjacence(graphe)
#laplacienne = creer_matrice_laplacienne(matrice)
#rang = calculer_rang(laplacienne)
#print("Rang de la matrice laplacienne :", rang)
#print("Connexité par algèbre linéaire :", rang == len(salles) - 1)


def calculer_lambda2(laplacienne):
    matrice = np.array(laplacienne, dtype=float)
    valeurs_propres = np.linalg.eigvalsh(matrice)
    lambda2 = valeurs_propres[1]

    return lambda2

#salles = generer_salles()
#graphe = creer_graphe(salles)
#matrice = creer_matrice_adjacence(graphe)
#laplacienne = creer_matrice_laplacienne(matrice)
#rang = calculer_rang(laplacienne)
#lambda2 = calculer_lambda2(laplacienne)
#print("Valeur de lambda 2 :", round(lambda2, 6))


def tester_ajout_connexions():
    graphe = {
        0: [1],
        1: [0, 2],
        2: [1, 3],
        3: [2, 4],
        4: [3, 5],
        5: [4, 6],
        6: [5, 7],
        7: [6]
    }
    connexions_a_ajouter = [
        (0, 7),
        (1, 6),
        (2, 5),
        (0, 4),
        (1, 5)
    ]
    print("----- AJOUT PROGRESSIF DE CONNEXIONS -----")
    for i in range(len(connexions_a_ajouter) + 1):
        matrice = creer_matrice_adjacence(graphe)
        laplacienne = creer_matrice_laplacienne(matrice)
        lambda2 = calculer_lambda2(laplacienne)
        nombre_connexions = 0
        for salle in graphe:
            nombre_connexions += len(graphe[salle])

        nombre_connexions = nombre_connexions // 2
        print("Nombre de connexions :", nombre_connexions)
        print("Lambda 2 :", round(lambda2, 6))
        print("--------------------")
        if i < len(connexions_a_ajouter):
            salle1, salle2 = connexions_a_ajouter[i]
            graphe[salle1].append(salle2)
            graphe[salle2].append(salle1)



def comparer_graphes():
    graphe_a = {
        0: [1, 7, 2],
        1: [0, 2],
        2: [1, 3, 0],
        3: [2, 4],
        4: [3, 5],
        5: [4, 6],
        6: [5, 7],
        7: [6, 0]
    }
    graphe_b = {
        0: [1, 7],
        1: [0, 2],
        2: [1, 3],
        3: [2, 4, 6],
        4: [3, 5],
        5: [4, 6],
        6: [5, 7, 3],
        7: [6, 0]
    }

    for nom, graphe in [("Graphe A", graphe_a), ("Graphe B", graphe_b)]:
        matrice = creer_matrice_adjacence(graphe)
        laplacienne = creer_matrice_laplacienne(matrice)
        lambda2 = calculer_lambda2(laplacienne)
        print(nom)
        print("Nombre de connexions :", sum(len(v) for v in graphe.values()) // 2)
        print("Lambda 2 :", round(lambda2, 6))
        print("--------------------")



def verifier_connexite(graphe, nombre_salles):
    visites = []
    a_visiter = [0]

    while len(a_visiter) > 0:
        salle = a_visiter.pop(0)
        if salle not in visites:
            visites.append(salle)
            for voisine in graphe[salle]:
                if voisine not in visites:
                    a_visiter.append(voisine)

    return len(visites) == nombre_salles


#salles = generer_salles()
#graphe = creer_graphe(salles)
#print(verifier_connexite(graphe, len(salles)))


def ajouter_connexions(graphe, nombre_salles):
    for i in range(nombre_salles):
        if random.random() < 0.25:
            voisine = random.randint(0, nombre_salles - 1)
            if voisine != i and voisine not in graphe[i]:
                graphe[i].append(voisine)
                graphe[voisine].append(i)

    return graphe


#salles = generer_salles()
#graphe = creer_graphe(salles)
#graphe = ajouter_connexions(graphe, len(salles))
#print(graphe)
#print(verifier_connexite(graphe, len(salles)))



#salles = generer_salles()
#graphe = creer_graphe(salles)
#graphe = ajouter_connexions(graphe, len(salles))
#couloirs = generer_couloirs(salles, graphe)
#carte = creer_carte(salles, couloirs)
#afficher_carte(carte)


def afficher_statistiques(salles, graphe, couloirs, carte):
    surface_totale = 0

    for salle in salles:
        surface = salle["largeur"] * salle["hauteur"]
        surface_totale += surface

    surface_moyenne = surface_totale / len(salles)
    nombre_connexions = 0

    for salle in graphe:
        nombre_connexions += len(graphe[salle])

    nombre_connexions = nombre_connexions // 2
    longueur_couloirs = 0

    for couloir in couloirs:
        longueur_couloirs += len(couloir) - 1

    nombre_cases_occupees = 0

    for ligne in carte:
        for case in ligne:
            if case != " ":
                nombre_cases_occupees += 1

    taux_occupation = nombre_cases_occupees / 1600 * 100

    print("----- STATISTIQUES DU DONJON -----")
    print("Nombre de salles :", len(salles))
    print("Surface totale des salles :", surface_totale)
    print("Surface moyenne des salles :", round(surface_moyenne, 2))
    print("Nombre de connexions :", nombre_connexions)
    print("Longueur totale des couloirs :", longueur_couloirs)
    print("Cases occupées :", nombre_cases_occupees)
    print("Taux d'occupation :", round(taux_occupation, 2), "%")


#salles = generer_salles()
#graphe = creer_graphe(salles)
#graphe = ajouter_connexions(graphe, len(salles))
#couloirs = generer_couloirs(salles, graphe)
#carte = creer_carte(salles, couloirs)
#afficher_statistiques(salles, graphe, couloirs, carte)


def verifier_limites(salles, couloirs):
    for salle in salles:
        if salle["x"] < 0 or salle["y"] < 0:
            return False
        if salle["x"] + salle["largeur"] > 40:
            return False
        if salle["y"] + salle["hauteur"] > 40:
            return False
        
    for couloir in couloirs:
        for x, y in couloir:
            if x < 0 or x >= 40 or y < 0 or y >= 40:
                return False

    return True


#salles = generer_salles()
#graphe = creer_graphe(salles)
#graphe = ajouter_connexions(graphe, len(salles))
#couloirs = generer_couloirs(salles, graphe)
#print("Limites respectées :", verifier_limites(salles, couloirs))


def experimenter_generations(nombre_generations):
    total_surface = 0
    total_occupation = 0
    total_connexions = 0
    total_longueur = 0
    valeurs_lambda2 = []
    echecs = 0

    for i in range(nombre_generations):
        salles = generer_salles()
        if salles is None:
            echecs += 1
            continue

        graphe = creer_graphe(salles)
        graphe = ajouter_connexions(graphe, len(salles))
        couloirs = generer_couloirs(salles, graphe)
        carte = creer_carte(salles, couloirs)
        surface = 0
        for salle in salles:
            surface += salle["largeur"] * salle["hauteur"]

        total_surface += surface / len(salles)
        cases_occupees = 0
        for ligne in carte:
            for case in ligne:
                if case != " ":
                    cases_occupees += 1

        total_occupation += cases_occupees / 1600 * 100
        connexions = 0
        for salle in graphe:
            connexions += len(graphe[salle])

        connexions = connexions // 2
        total_connexions += connexions
        longueur = 0
        for couloir in couloirs:
            longueur += len(couloir) - 1

        total_longueur += longueur
        matrice = creer_matrice_adjacence(graphe)
        laplacienne = creer_matrice_laplacienne(matrice)
        lambda2 = calculer_lambda2(laplacienne)
        valeurs_lambda2.append(lambda2)

    generations_reussies = nombre_generations - echecs
    if generations_reussies == 0:
        print("Aucune génération réussie.")
        return

    moyenne_lambda2 = sum(valeurs_lambda2) / generations_reussies
    lambda2_min = min(valeurs_lambda2)
    lambda2_max = max(valeurs_lambda2)

    print("----- EXPERIMENTATION -----")
    print("Générations demandées :", nombre_generations)
    print("Générations réussies :", generations_reussies)
    print("Échecs :", echecs)
    print("Surface moyenne des salles :",
          round(total_surface / generations_reussies, 2))
    print("Taux d'occupation moyen :",
          round(total_occupation / generations_reussies, 2), "%")
    print("Nombre moyen de connexions :",
          round(total_connexions / generations_reussies, 2))
    print("Longueur moyenne des couloirs :",
          round(total_longueur / generations_reussies, 2))
    print("Lambda 2 moyen :", round(moyenne_lambda2, 6))
    print("Lambda 2 minimum :", round(lambda2_min, 6))
    print("Lambda 2 maximum :", round(lambda2_max, 6))



def tester_rang():
    graphe1 = {
        0: [1],
        1: [0, 2],
        2: [1]
    }
    graphe2 = {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1]
    }
    graphe3 = {
        0: [1],
        1: [0],
        2: []
    }
    for numero, graphe in enumerate([graphe1, graphe2, graphe3], start=1):
        matrice = creer_matrice_adjacence(graphe)
        laplacienne = creer_matrice_laplacienne(matrice)
        rang = calculer_rang(laplacienne)
        lambda2 = calculer_lambda2(laplacienne)
        print("Valeur de lambda 2 :", round(lambda2, 6))
        print("TEST", numero)
        print("Rang :", rang)
        print("Connexe :", rang == len(graphe) - 1)
        print("--------------------")



def main():
    salles = generer_salles()

    if salles is not None:
        graphe = creer_graphe(salles)
        graphe = ajouter_connexions(graphe, len(salles))
        couloirs = generer_couloirs(salles, graphe)
        carte = creer_carte(salles, couloirs)

        afficher_carte(carte)
        afficher_statistiques(salles, graphe, couloirs, carte)

        matrice = creer_matrice_adjacence(graphe)
        laplacienne = creer_matrice_laplacienne(matrice)
        rang = calculer_rang(laplacienne)
        lambda2 = calculer_lambda2(laplacienne)
        print("----- ANALYSE MATHEMATIQUE -----")
        print("Rang de la matrice laplacienne :", rang)
        print("Connexité par le rang :", rang == len(salles) - 1)
        print("Valeur de lambda 2 :", round(lambda2, 6))
        print("Connexité par lambda 2 :", lambda2 > 1e-10)
        print("Limites respectées :", verifier_limites(salles, couloirs))
    else:
        print("Impossible de générer le donjon.")



#tester_rang()
#tester_ajout_connexions()
#comparer_graphes()
#experimenter_generations(100)

if __name__ == "__main__":
    main()
