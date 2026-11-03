# Outils fondamentaux – BUT Informatique

Ce dépôt regroupe les travaux pratiques et le projet réalisés dans le cadre de la matière **Outils fondamentaux**.

## Arborescence

```text
Outils-Fondamentaux-TP/
├── Générateur_Donjon/
│   ├── Projet.py
│   ├── test_projet.py
│   └── requirements.txt
├── TP/
│   ├── TP1.py
│   ├── TP2.py
│   ├── TP3.py
│   ├── TP4.py
│   └── TP5.py
└── README.md
```

Le dossier `TP/` regroupe les travaux pratiques. Le projet personnel et ses tests se trouvent dans `Générateur_Donjon/`.

## Projet : générateur de donjons

Le programme génère une carte de 40 × 40 cases composée de huit salles rectangulaires sans chevauchement, reliées par des couloirs. Il affiche la carte, des statistiques géométriques et des indicateurs de connexité du graphe des salles.

### Notions mathématiques

- La matrice d'adjacence représente les connexions entre les salles.
- La matrice laplacienne est calculée selon $L = D - A$.
- Le rang est calculé par élimination de Gauss avec une tolérance configurable dans l'expérience numérique.
- Les valeurs propres sont calculées par rotations de Jacobi ; NumPy sert de référence indépendante dans les tests.
- Pour un graphe non orienté, la multiplicité de la valeur propre nulle du Laplacien correspond au nombre de composantes connexes. Ainsi, un graphe est connexe si son rang vaut $n - 1$ et si λ₂ est strictement positive, à la précision numérique près.

### Expériences et interprétation

Pour comparer des structures à taille et nombre d'arêtes constants, l'expérience ci-dessous construit cinq graphes de huit sommets et dix arêtes :

```powershell
python Générateur_Donjon/Projet.py --experimenter-graphes
```

Quatre graphes sont connexes ; le cinquième est une clique K5 accompagnée de trois sommets isolés. Les valeurs obtenues sont :

|Structure|Arêtes|Connexe|Rang du Laplacien|λ₂|
|---|---:|---:|---:|---:|
|Cycle avec deux cordes|10|Oui|7|0,763932|
|Échelle 2×4|10|Oui|7|0,585786|
|Deux cycles reliés par deux arêtes|10|Oui|7|0,585786|
|Clique K4 reliée à une chaîne|10|Oui|7|0,202257|
|Clique K5 et trois sommets isolés|10|Non|4|0|

Le nombre d'arêtes, à lui seul, ne détermine donc pas la connexité ni la valeur de λ₂. Parmi ces exemples connexes, le cycle avec deux cordes a le λ₂ le plus élevé : il présente la plus forte connectivité algébrique selon cet indicateur. λ₂ ne décrit toutefois pas à lui seul la géométrie des couloirs ni tous les scénarios de panne possibles.

### Résistance à la suppression d'une arête

L'expérience supprime chaque arête, une à la fois, sur une copie du graphe. Elle compte les ponts (arêtes dont la suppression déconnecte le graphe) et relève le λ₂ minimal après suppression :

```powershell
python Générateur_Donjon/Projet.py --experimenter-suppressions
```

|Structure connexe|λ₂ initial|Ponts|λ₂ minimal après une suppression|
|---|---:|---:|---:|
|Cycle avec deux cordes|0,763932|0|0,363595|
|Échelle 2×4|0,585786|0|0,290725|
|Deux cycles reliés par deux arêtes|0,585786|0|0,290725|
|Clique K4 reliée à une chaîne|0,202257|4|0|

Dans ces exemples, les trois premières structures restent connexes après la perte d'une arête. La chaîne attachée à la clique possède quatre ponts : supprimer l'un d'eux déconnecte le graphe et annule λ₂. Cela illustre pourquoi un même nombre de connexions ne garantit pas la même résistance aux coupures. L'étude porte sur des graphes de petite taille et sur la panne d'une arête à la fois.

L'expérience sur la tolérance utilise une matrice presque singulière et montre que le rang numérique dépend du seuil choisi :

```powershell
python Générateur_Donjon/Projet.py --experimenter-tolerance
```

Enfin, une génération aléatoire conserve volontairement une chaîne d'arêtes comme structure de base ; ses graphes sont donc toujours connexes. Les statistiques distinguent les deux états, mais les graphes déconnectés sont étudiés dans l'expérience comparative plutôt que dans les générations normales.

### Installation et lancement

Le générateur utilise la bibliothèque standard. NumPy est nécessaire aux tests de comparaison ; l'installer depuis la racine du dépôt avec :

```powershell
pip install -r Générateur_Donjon/requirements.txt
```

Générer et afficher un donjon :

```powershell
python Générateur_Donjon/Projet.py
```

Lancer 100 générations avec une graine reproductible :

```powershell
python Générateur_Donjon/Projet.py --experimenter-generations 100 --seed 42
```

Exécuter les tests, dont la comparaison des valeurs propres avec NumPy :

```powershell
python -m unittest discover -s Générateur_Donjon -p "test_*.py"
```

### Limites

- Le rang et les valeurs propres sont des calculs en virgule flottante ; les seuils choisis peuvent affecter les cas proches de zéro.
- La génération de salles est aléatoire et peut échouer après un nombre limité d'essais.
- Les couloirs suivent un tracé horizontal puis vertical entre les centres des salles ; ils ne sont pas optimisés pour éviter les autres salles ou couloirs.
- Les expériences portent sur de petits graphes et ne suffisent pas à généraliser à toutes les topologies.

### Utilisation de l'intelligence artificielle

Une IA a été utilisée comme outil d'assistance ponctuel. Les choix de conception, le développement et les vérifications du programme ont été réalisés et validés personnellement.
