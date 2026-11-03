# Générateur de donjons en Python

## Présentation

Ce projet consiste à développer un générateur automatique de donjons en Python dans le cadre d'un projet universitaire.

Le programme génère une carte de 40 × 40 cases composée de salles rectangulaires reliées entre elles par des couloirs.

## Fonctionnalités

- Génération aléatoire de 8 salles.
- Vérification du chevauchement entre les salles.
- Création de couloirs entre les salles.
- Représentation du donjon sous forme de matrice.
- Affichage du donjon dans le terminal.
- Calcul de statistiques sur les générations.
- Vérification des limites de la carte.

## Partie mathématique

Le projet utilise plusieurs notions mathématiques :

- Matrice d'adjacence pour représenter les connexions.
- Matrice laplacienne avec la formule L = D - A.
- Pivot de Gauss pour calculer le rang.
- Vérification de la connexité à partir du rang de la matrice laplacienne.
- Calcul de la deuxième plus petite valeur propre λ₂ pour étudier la connectivité algébrique.

## Expérimentations

Une expérimentation sur 100 générations a donné les résultats suivants :

|Indicateur|Résultat|
|---|---|
|Générations réussies|100 / 100|
|Surface moyenne des salles|46,13|
|Taux d'occupation moyen|29,51 %|
|Nombre moyen de connexions|8,14|
|Longueur moyenne des couloirs|202,16|
|λ₂ moyenne|0,327861|
|λ₂ minimale|0,152241|
|λ₂ maximale|1,139194|

## Installation

Python 3 et NumPy sont nécessaires.

Installer les dépendances avec :

```
pip install -r requirements.txt
```

## Exécution

Lancer le programme avec :

```
python Projet.py
```