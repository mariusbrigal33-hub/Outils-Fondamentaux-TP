import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import hdbscan
import umap
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.datasets import make_moons
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA


def genere_clients():
    rng = np.random.default_rng(0)
    centres = [(25, 20), (25, 80), (45, 50), (65, 20), (65, 80)]
    morceaux = []
    vrais_groupes = []

    for i, (cx, cy) in enumerate(centres):
        age = rng.normal(30, 6, 60)
        revenu = rng.normal(cx * 1000, 8000, 60)
        score = rng.normal(cy, 10, 60).clip(1, 100)
        morceaux.append(pd.DataFrame({
            "age": age,
            "revenu": revenu,
            "score_depense": score
        }))
        vrais_groupes += [i] * 60

    clients = pd.concat(morceaux, ignore_index=True)
    X = clients[["age", "revenu", "score_depense"]].values
    Xs = StandardScaler().fit_transform(X)

    return clients, X, Xs, vrais_groupes


def etape1_kmeans():
    clients, X, Xs, vrais_groupes = genere_clients()

    km_brut = KMeans(n_clusters=5, random_state=42, n_init=10).fit(X)
    km_norm = KMeans(n_clusters=5, random_state=42, n_init=10).fit(Xs)

    print("Sans normalisation :", round(adjusted_rand_score(vrais_groupes, km_brut.labels_), 3))
    print("Avec normalisation :", round(adjusted_rand_score(vrais_groupes, km_norm.labels_), 3))


def exercice1_1():
    X, y = make_moons(n_samples=500, noise=0.1, random_state=42)
    labels = KMeans(n_clusters=2, random_state=42, n_init=10).fit_predict(X)
    print("ARI K-Means :", round(adjusted_rand_score(y, labels), 3))


def etape2_dbscan():
    X, y = make_moons(n_samples=500, noise=0.1, random_state=42)
    labels = DBSCAN(eps=0.2, min_samples=5).fit_predict(X)

    print("ARI DBSCAN :", round(adjusted_rand_score(y, labels), 3))
    print("Clusters trouvés :", sorted(set(labels)))


def exercice2_1():
    X, y = make_moons(n_samples=500, noise=0.1, random_state=42)
    voisins = NearestNeighbors(n_neighbors=5).fit(X)
    distances, indices = voisins.kneighbors(X)

    plt.plot(np.sort(distances[:, 4]))
    plt.xlabel("Points triés")
    plt.ylabel("Distance au 5e voisin")
    plt.title("Graphe des k-distances")
    plt.show()


def etape3_silhouette():
    clients, X, Xs, vrais_groupes = genere_clients()
    resultats = []

    for k in range(2, 9):
        km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(Xs)
        resultats.append((k, km.inertia_, silhouette_score(Xs, km.labels_)))

    for k, inertie, silhouette in resultats:
        print(f"k={k} : inertie={inertie:.1f}, silhouette={silhouette:.3f}")


def exercice3_1():
    clients, X, Xs, vrais_groupes = genere_clients()
    resultats = []

    for k in range(2, 9):
        labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(Xs)
        resultats.append((k, silhouette_score(Xs, labels)))

    meilleur = max(resultats, key=lambda resultat: resultat[1])

    print("Meilleur k :", meilleur[0])
    print("Score :", round(meilleur[1], 3))
    print("Nombre réel de groupes :", 5)


def etape4_hdbscan():
    clients, X, Xs, vrais_groupes = genere_clients()

    km = KMeans(n_clusters=5, random_state=42, n_init=10).fit(Xs)
    labels = hdbscan.HDBSCAN(min_cluster_size=15, min_samples=5).fit_predict(Xs)

    print("Clusters HDBSCAN :", sorted(set(labels)))
    print(pd.Series(labels).value_counts())
    print("ARI HDBSCAN :", round(adjusted_rand_score(vrais_groupes, labels), 3))
    print("ARI K-Means :", round(adjusted_rand_score(vrais_groupes, km.labels_), 3))


def exercice4_1():
    clients, X, Xs, vrais_groupes = genere_clients()
    labels = hdbscan.HDBSCAN(min_cluster_size=15, min_samples=5).fit_predict(Xs)

    clusters = set(labels)
    clusters.discard(-1)

    print("Nombre de clusters :", len(clusters))
    print("Nombre de points de bruit :", sum(labels == -1))


def etape5_reduction_dimension():
    clients, X, Xs, vrais_groupes = genere_clients()
    labels = KMeans(n_clusters=5, random_state=42, n_init=10).fit_predict(Xs)

    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(Xs)
    X_umap = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42).fit_transform(Xs)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap="tab10", alpha=0.7)
    axes[0].set_title("PCA")
    axes[1].scatter(X_umap[:, 0], X_umap[:, 1], c=labels, cmap="tab10", alpha=0.7)
    axes[1].set_title("UMAP")

    plt.tight_layout()
    plt.show()


def exercice5_1():
    clients, X, Xs, vrais_groupes = genere_clients()
    pca = PCA(n_components=2, random_state=42)
    pca.fit_transform(Xs)

    print("Variance expliquée :", pca.explained_variance_ratio_)
    print("Variance totale expliquée :", pca.explained_variance_ratio_.sum())

