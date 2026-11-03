import unicodedata
import random
from math import gcd
from collections import Counter


def lettre_vers_nombre(c):
    return ord(c) - ord("A")


def nombre_vers_lettre(n):
    return chr(ord("A") + n % 26)


def nettoyer(texte):
    texte = texte.upper()
    texte = unicodedata.normalize("NFD", texte)

    resultat = ""

    for c in texte:
        if unicodedata.category(c) != "Mn" and "A" <= c <= "Z":
            resultat += c

    return resultat


def chiffrer(texte, a, b):
    if gcd(a, 26) != 1:
        raise ValueError("Clé invalide : a doit être premier avec 26.")

    resultat = ""

    for c in texte:
        nombre = lettre_vers_nombre(c)
        nouveau_nombre = (a * nombre + b) % 26
        resultat += nombre_vers_lettre(nouveau_nombre)

    return resultat


def cles_utilisables():
    cles = []

    for a in range(1, 26):
        if gcd(a, 26) == 1:
            cles.append(a)

    print("Valeurs de a utilisables :", cles)
    print("Nombre de valeurs :", len(cles))

    return cles


def inverse_modulaire(a, n):
    for i in range(1, n):
        if (a * i) % n == 1:
            return i

    raise ValueError("Cet inverse modulaire n'existe pas.")


def exemple_cle_invalide():
    try:
        inverse = inverse_modulaire(4, 26)
        print("Inverse :", inverse)
    except ValueError as erreur:
        print("Erreur :", erreur)


def dechiffrer(texte, a, b):
    inverse = inverse_modulaire(a, 26)
    resultat = ""

    for c in texte:
        nombre = lettre_vers_nombre(c)
        nouveau_nombre = (inverse * (nombre - b)) % 26
        resultat += nombre_vers_lettre(nouveau_nombre)

    return resultat


def toutes_les_clefs(secret):
    propositions = []
    cles = cles_utilisables()

    for a in cles:
        for b in range(26):
            message = dechiffrer(secret, a, b)
            propositions.append((a, b, message))

    print("Nombre de clés essayées :", len(propositions))

    for a, b, message in propositions:
        print("Clé :", a, b, "| Message :", message)

    return propositions


def casser_frequences(secret):
    frequences = Counter(secret)
    lettre_plus_frequente = frequences.most_common(1)[0][0]

    print("Lettre la plus fréquente :", lettre_plus_frequente)

    propositions = []

    for a in cles_utilisables():
        b = (lettre_vers_nombre(lettre_plus_frequente) - a * lettre_vers_nombre("E")) % 26
        message = dechiffrer(secret, a, b)
        propositions.append((a, b, message))

        print("Clé :", a, b, "| Message :", message)

    return propositions


def indice_coincidence(texte):
    longueur = len(texte)

    if longueur < 2:
        return 0

    frequences = Counter(texte)
    total = 0

    for nombre in frequences.values():
        total += nombre * (nombre - 1)

    return total / (longueur * (longueur - 1))


def vigenere(texte, cle):
    resultat = ""

    for i in range(len(texte)):
        nombre_texte = lettre_vers_nombre(texte[i])
        nombre_cle = lettre_vers_nombre(cle[i % len(cle)])
        nouveau_nombre = (nombre_texte + nombre_cle) % 26

        resultat += nombre_vers_lettre(nouveau_nombre)

    return resultat


def longueur_cle_vigenere(secret):
    for longueur in range(1, 8):
        indices = []

        for i in range(longueur):
            colonne = secret[i::longueur]
            indices.append(indice_coincidence(colonne))

        moyenne = sum(indices) / len(indices)

        print("Longueur :", longueur, "| Indice moyen :", round(moyenne, 3))


