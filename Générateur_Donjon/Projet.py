import argparse
import random
from collections import deque


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

def creer_couloir(salle1: dict[str, int], salle2: dict[str, int]) -> list[tuple[int, int]]:
    """Construit un couloir en L entre les centres de deux salles."""
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


def generer_couloirs(
    salles: list[dict[str, int]],
    graphe: dict[int, list[int]],
) -> list[list[tuple[int, int]]]:
    """Construit un couloir pour chaque arête non orientée du graphe."""
    couloirs = []
    for salle in graphe:
        for voisine in graphe[salle]:
            if salle < voisine:
                couloir = creer_couloir(salles[salle], salles[voisine])
                couloirs.append(couloir)

    return couloirs

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

def creer_graphe(salles: list[dict[str, int]]) -> dict[int, list[int]]:
    """Relie les salles en chaîne pour garantir la connexité initiale."""
    graphe = {}

    for i in range(len(salles)):
        graphe[i] = []
    for i in range(len(salles) - 1):
        graphe[i].append(i + 1)
        graphe[i + 1].append(i)

    return graphe

def creer_matrice_adjacence(graphe: dict[int, list[int]]) -> list[list[int]]:
    """Convertit un graphe non orienté en matrice d'adjacence."""
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


def creer_matrice_laplacienne(matrice: list[list[int]]) -> list[list[int]]:
    """Construit le Laplacien combinatoire L = D - A."""
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

def calculer_rang(matrice: list[list[float]], tolerance: float = 1e-10) -> int:
    """Calcule le rang numerique par elimination de Gauss avec pivot partiel."""
    nombre_lignes = len(matrice)
    if nombre_lignes == 0:
        return 0
    nombre_colonnes = len(matrice[0])
    if tolerance < 0:
        raise ValueError("La tolérance doit être positive ou nulle.")
    if any(len(ligne) != nombre_colonnes for ligne in matrice):
        raise ValueError("Toutes les lignes doivent avoir la même longueur.")
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

def calculer_valeurs_propres_jacobi(
    matrice: list[list[float]],
    tolerance: float = 1e-12,
    iterations_max: int = 10000,
) -> list[float]:
    """Calcule les valeurs propres d'une matrice symetrique par rotations de Jacobi."""
    nombre_lignes = len(matrice)
    if nombre_lignes == 0 or any(len(ligne) != nombre_lignes for ligne in matrice):
        raise ValueError("La matrice doit être carrée et non vide.")
    if tolerance <= 0:
        raise ValueError("La tolérance doit être positive.")
    if not isinstance(iterations_max, int) or isinstance(iterations_max, bool) or iterations_max < 1:
        raise ValueError("Le nombre maximal d'iterations doit etre un entier positif.")

    resultat = [[float(valeur) for valeur in ligne] for ligne in matrice]
    for i in range(nombre_lignes):
        for j in range(i + 1, nombre_lignes):
            if abs(resultat[i][j] - resultat[j][i]) > tolerance:
                raise ValueError("La matrice doit être symétrique.")

    for _ in range(iterations_max):
        p, q = 0, 0
        plus_grand = 0.0
        for i in range(nombre_lignes):
            for j in range(i + 1, nombre_lignes):
                if abs(resultat[i][j]) > plus_grand:
                    p, q = i, j
                    plus_grand = abs(resultat[i][j])

        if plus_grand <= tolerance:
            return sorted(resultat[i][i] for i in range(nombre_lignes))

        app = resultat[p][p]
        aqq = resultat[q][q]
        apq = resultat[p][q]
        tau = (aqq - app) / (2 * apq)
        signe = 1.0 if tau >= 0 else -1.0
        t = signe / (abs(tau) + (1 + tau * tau) ** 0.5)
        cosinus = 1 / (1 + t * t) ** 0.5
        sinus = t * cosinus

        resultat[p][p] = app - t * apq
        resultat[q][q] = aqq + t * apq
        resultat[p][q] = 0.0
        resultat[q][p] = 0.0

        for k in range(nombre_lignes):
            if k != p and k != q:
                akp = resultat[k][p]
                akq = resultat[k][q]
                resultat[k][p] = cosinus * akp - sinus * akq
                resultat[p][k] = resultat[k][p]
                resultat[k][q] = sinus * akp + cosinus * akq
                resultat[q][k] = resultat[k][q]
    raise RuntimeError("La méthode de Jacobi n'a pas convergé.")


def calculer_lambda2(laplacienne: list[list[float]]) -> float:
    """Renvoie la deuxieme plus petite valeur propre du Laplacien."""
    valeurs_propres = calculer_valeurs_propres_jacobi(laplacienne)
    if len(valeurs_propres) < 2:
        raise ValueError("Il faut au moins deux sommets pour calculer lambda 2.")
    return valeurs_propres[1]

def verifier_connexite(graphe: dict[int, list[int]], nombre_salles: int) -> bool:
    """Teste si tous les sommets du graphe sont accessibles depuis le sommet 0."""
    if nombre_salles == 0:
        return True
    if 0 not in graphe:
        return False

    visites = {0}
    a_visiter = deque([0])
    while a_visiter:
        salle = a_visiter.popleft()
        for voisine in graphe[salle]:
            if voisine not in graphe:
                return False
            if voisine not in visites:
                visites.add(voisine)
                a_visiter.append(voisine)

    return len(visites) == nombre_salles


def creer_graphe_depuis_aretes(
    nombre_sommets: int,
    aretes: list[tuple[int, int]],
) -> dict[int, list[int]]:
    """Construit un graphe non oriente et refuse les aretes invalides ou dupliquees."""
    if not isinstance(nombre_sommets, int) or isinstance(nombre_sommets, bool) or nombre_sommets < 0:
        raise ValueError("Le nombre de sommets doit etre un entier positif ou nul.")
    graphe = {i: [] for i in range(nombre_sommets)}
    for salle1, salle2 in aretes:
        if salle1 not in graphe or salle2 not in graphe or salle1 == salle2:
            raise ValueError("Chaque arête doit relier deux sommets distincts existants.")
        if salle2 in graphe[salle1]:
            raise ValueError("Les arêtes du graphe doivent être uniques.")
        graphe[salle1].append(salle2)
        graphe[salle2].append(salle1)
    return graphe


def creer_graphes_experimentaux():
    cycle_avec_cordes = [(i, (i + 1) % 8) for i in range(8)]
    cycle_avec_cordes.extend([(0, 4), (1, 5)])

    echelle = [(i, i + 1) for i in range(3)]
    echelle.extend((i + 4, i + 5) for i in range(3))
    echelle.extend((i, i + 4) for i in range(4))

    deux_cycles = [(0, 1), (1, 2), (2, 3), (3, 0)]
    deux_cycles.extend([(4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5)])
    clique_et_isoles = [(i, j) for i in range(5) for j in range(i + 1, 5)]
    clique_et_chaine = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    clique_et_chaine.extend([(3, 4), (4, 5), (5, 6), (6, 7)])

    return {
        "Cycle avec deux cordes": creer_graphe_depuis_aretes(8, cycle_avec_cordes),
        "Echelle 2x4": creer_graphe_depuis_aretes(8, echelle),
        "Deux cycles relies par deux aretes": creer_graphe_depuis_aretes(8, deux_cycles),
        "Clique K4 reliee a une chaine": creer_graphe_depuis_aretes(8, clique_et_chaine),
        "Clique K5 et trois sommets isoles": creer_graphe_depuis_aretes(8, clique_et_isoles),
    }


def experimenter_graphes():
    print("----- COMPARAISON DE GRAPHES A 8 SOMMETS ET 10 ARETES -----")
    for nom, graphe in creer_graphes_experimentaux().items():
        matrice = creer_matrice_adjacence(graphe)
        laplacienne = creer_matrice_laplacienne(matrice)
        rang = calculer_rang(laplacienne)
        lambda2 = calculer_lambda2(laplacienne)
        nombre_aretes = sum(len(voisins) for voisins in graphe.values()) // 2
        connexe = verifier_connexite(graphe, len(graphe))
        print(nom)
        print("Nombre d'aretes :", nombre_aretes)
        print("Graphe connexe :", connexe)
        print("Rang du Laplacien :", rang)
        print("lambda 2 :", round(lambda2, 6))
        print("--------------------")


def analyser_suppressions_aretes(graphe: dict[int, list[int]]) -> dict[str, object]:
    """Mesure les ponts et le lambda 2 minimal apres suppression de chaque arete."""
    nombre_sommets = len(graphe)
    if not verifier_connexite(graphe, nombre_sommets):
        raise ValueError("L'analyse de suppression exige un graphe initial connexe.")

    aretes = [
        (salle, voisine)
        for salle, voisines in graphe.items()
        for voisine in voisines
        if salle < voisine
    ]
    lambda2_initial = calculer_lambda2(
        creer_matrice_laplacienne(creer_matrice_adjacence(graphe))
    )
    suppressions = []

    for salle1, salle2 in aretes:
        graphe_modifie = {salle: voisines[:] for salle, voisines in graphe.items()}
        graphe_modifie[salle1].remove(salle2)
        graphe_modifie[salle2].remove(salle1)
        connexe = verifier_connexite(graphe_modifie, nombre_sommets)
        laplacienne = creer_matrice_laplacienne(creer_matrice_adjacence(graphe_modifie))
        lambda2 = calculer_lambda2(laplacienne)
        suppressions.append({
            "arete": (salle1, salle2),
            "connexe": connexe,
            "lambda2": lambda2,
        })

    ponts = [resultat["arete"] for resultat in suppressions if not resultat["connexe"]]
    return {
        "lambda2_initial": lambda2_initial,
        "nombre_aretes_testees": len(aretes),
        "ponts": ponts,
        "lambda2_min_apres_suppression": min(
            resultat["lambda2"] for resultat in suppressions
        ) if suppressions else lambda2_initial,
        "suppressions_deconnectantes": len(ponts),
    }


def experimenter_suppressions_aretes() -> None:
    """Compare la resilience des topologies connexes de l'experience."""
    print("----- RESISTANCE A LA SUPPRESSION D'UNE ARETE -----")
    for nom, graphe in creer_graphes_experimentaux().items():
        if not verifier_connexite(graphe, len(graphe)):
            continue
        resultat = analyser_suppressions_aretes(graphe)
        print(nom)
        print("lambda 2 initial :", round(resultat["lambda2_initial"], 6))
        print("Aretes testees :", resultat["nombre_aretes_testees"])
        print("Ponts :", resultat["ponts"])
        print("Suppressions deconnectantes :", resultat["suppressions_deconnectantes"])
        print("lambda 2 minimal apres suppression :",
              round(resultat["lambda2_min_apres_suppression"], 6))
        print("--------------------")


def experimenter_tolerance():
    matrice = [[1.0, 1.0], [1.0, 1.0 + 1e-11]]
    print("----- INFLUENCE DE LA TOLERANCE SUR LE RANG -----")
    for tolerance in (1e-8, 1e-10, 1e-12, 1e-14):
        print("Tolerance :", tolerance, "| rang :", calculer_rang(matrice, tolerance))

def ajouter_connexions(graphe, nombre_salles):
    for i in range(nombre_salles):
        if random.random() < 0.25:
            voisine = random.randint(0, nombre_salles - 1)
            if voisine != i and voisine not in graphe[i]:
                graphe[i].append(voisine)
                graphe[voisine].append(i)

    return graphe

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
    print("Graphe connexe :", verifier_connexite(graphe, len(salles)))
    print("Longueur totale des couloirs :", longueur_couloirs)
    print("Cases occupées :", nombre_cases_occupees)
    print("Taux d'occupation :", round(taux_occupation, 2), "%")

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

def experimenter_generations(nombre_generations: int) -> None:
    """Affiche des statistiques agregees sur plusieurs donjons aleatoires."""
    total_surface = 0
    total_occupation = 0
    total_connexions = 0
    total_longueur = 0
    valeurs_lambda2 = []
    generations_connexes = 0
    generations_deconnectees = 0
    lambda2_connexes = []
    lambda2_deconnectees = []
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
        if verifier_connexite(graphe, len(salles)):
            generations_connexes += 1
            lambda2_connexes.append(lambda2)
        else:
            generations_deconnectees += 1
            lambda2_deconnectees.append(lambda2)

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
    print("Générations connexes :", generations_connexes)
    print("Générations déconnectées :", generations_deconnectees)
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
    if lambda2_connexes:
        print("Lambda 2 moyen des graphes connexes :",
              round(sum(lambda2_connexes) / len(lambda2_connexes), 6))
    if lambda2_deconnectees:
        print("Lambda 2 moyen des graphes déconnectés :",
              round(sum(lambda2_deconnectees) / len(lambda2_deconnectees), 6))



def main() -> None:
    """Lance le mode graphique par defaut ou une experience choisie en CLI."""
    analyseur = argparse.ArgumentParser(description="Generateur et analyseur de donjons.")
    modes = analyseur.add_mutually_exclusive_group()
    modes.add_argument("--experimenter-generations", type=int, metavar="N")
    modes.add_argument("--experimenter-graphes", action="store_true")
    modes.add_argument("--experimenter-tolerance", action="store_true")
    modes.add_argument("--experimenter-suppressions", action="store_true")
    analyseur.add_argument("--seed", type=int, help="Graine aleatoire pour reproduire une generation.")
    arguments = analyseur.parse_args()

    if arguments.seed is not None:
        random.seed(arguments.seed)
    if arguments.experimenter_generations is not None:
        if arguments.experimenter_generations < 1:
            analyseur.error("N doit etre strictement positif.")
        experimenter_generations(arguments.experimenter_generations)
        return
    if arguments.experimenter_graphes:
        experimenter_graphes()
        return
    if arguments.experimenter_tolerance:
        experimenter_tolerance()
        return
    if arguments.experimenter_suppressions:
        experimenter_suppressions_aretes()
        return

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



if __name__ == "__main__":
    main()
