import unittest
import numpy as np
import Projet


class TestsAnalyseGraphes(unittest.TestCase):
    def test_valeurs_propres_jacobi_contre_numpy(self):
        laplaciennes = [
            [[1, -1, 0], [-1, 2, -1], [0, -1, 1]],
            [[2, -1, -1], [-1, 2, -1], [-1, -1, 2]],
            [[1, -1, 0], [-1, 1, 0], [0, 0, 0]],
        ]
        generateur = np.random.default_rng(42)
        for taille in range(2, 9):
            matrice = generateur.normal(size=(taille, taille))
            laplaciennes.append(((matrice + matrice.T) / 2).tolist())

        for matrice in laplaciennes:
            with self.subTest(taille=len(matrice)):
                valeurs_jacobi = Projet.calculer_valeurs_propres_jacobi(matrice)
                valeurs_numpy = np.linalg.eigvalsh(np.array(matrice, dtype=float))
                np.testing.assert_allclose(valeurs_jacobi, valeurs_numpy, atol=1e-10)

    def test_lambda2_connexe_et_deconnecte(self):
        chemin = [[1, -1, 0], [-1, 2, -1], [0, -1, 1]]
        triangle = [[2, -1, -1], [-1, 2, -1], [-1, -1, 2]]
        deconnecte = [[1, -1, 0], [-1, 1, 0], [0, 0, 0]]

        self.assertAlmostEqual(Projet.calculer_lambda2(chemin), 1.0)
        self.assertAlmostEqual(Projet.calculer_lambda2(triangle), 3.0)
        self.assertAlmostEqual(Projet.calculer_lambda2(deconnecte), 0.0)

    def test_tolerance_influence_le_rang_numerique(self):
        matrice = [[1.0, 1.0], [1.0, 1.0 + 1e-11]]
        tolerances = (1e-8, 1e-10, 1e-12, 1e-14)
        rangs = [Projet.calculer_rang(matrice, tolerance) for tolerance in tolerances]

        self.assertEqual(rangs, [1, 1, 2, 2])

    def test_graphes_experimentaux_ont_le_meme_nombre_d_aretes(self):
        graphes = Projet.creer_graphes_experimentaux()
        connexites = []

        for graphe in graphes.values():
            self.assertEqual(len(graphe), 8)
            self.assertEqual(sum(map(len, graphe.values())) // 2, 10)
            connexites.append(Projet.verifier_connexite(graphe, len(graphe)))

        self.assertEqual(connexites, [True, True, True, True, False])

    def test_rang_et_lambda2_identifient_le_graphe_deconnecte(self):
        graphe = Projet.creer_graphes_experimentaux()[
            "Clique K5 et trois sommets isoles"
        ]
        laplacienne = Projet.creer_matrice_laplacienne(
            Projet.creer_matrice_adjacence(graphe)
        )

        self.assertEqual(Projet.calculer_rang(laplacienne), 4)
        self.assertAlmostEqual(Projet.calculer_lambda2(laplacienne), 0.0)

    def test_jacobi_refuse_les_matrices_invalides(self):
        with self.assertRaises(ValueError):
            Projet.calculer_valeurs_propres_jacobi([[1, 2], [3]])
        with self.assertRaises(ValueError):
            Projet.calculer_valeurs_propres_jacobi([[1, 1], [0, 2]])

    def test_jacobi_refuse_un_nombre_d_iterations_invalide(self):
        for iterations in (0, -1, 1.5, True):
            with self.subTest(iterations=iterations):
                with self.assertRaises(ValueError):
                    Projet.calculer_valeurs_propres_jacobi(
                        [[1, 0], [0, 2]], iterations_max=iterations
                    )

    def test_creation_graphe_refuse_aretes_invalides(self):
        entrees_invalides = (
            [(0, 1), (0, 1)],
            [(0, 1), (1, 0)],
            [(0, 2)],
            [(1, 1)],
        )
        for aretes in entrees_invalides:
            with self.subTest(aretes=aretes):
                with self.assertRaises(ValueError):
                    Projet.creer_graphe_depuis_aretes(2, aretes)

    def test_connexite_refuse_un_voisin_inexistant(self):
        graphe = {0: [1], 1: [0, 2]}
        self.assertFalse(Projet.verifier_connexite(graphe, 2))

    def test_lambda2_refuse_un_graphe_a_un_seul_sommet(self):
        with self.assertRaises(ValueError):
            Projet.calculer_lambda2([[0]])

    def test_suppression_aretes_identifie_les_ponts_sans_modifier_graphe(self):
        graphes = Projet.creer_graphes_experimentaux()
        robuste = graphes["Cycle avec deux cordes"]
        fragile = graphes["Clique K4 reliee a une chaine"]
        robuste_initial = {sommet: voisins[:] for sommet, voisins in robuste.items()}
        fragile_initial = {sommet: voisins[:] for sommet, voisins in fragile.items()}

        resultat_robuste = Projet.analyser_suppressions_aretes(robuste)
        resultat_fragile = Projet.analyser_suppressions_aretes(fragile)

        self.assertEqual(resultat_robuste["ponts"], [])
        self.assertGreater(resultat_robuste["lambda2_min_apres_suppression"], 0)
        self.assertEqual(len(resultat_fragile["ponts"]), 4)
        self.assertEqual(resultat_fragile["suppressions_deconnectantes"], 4)
        self.assertAlmostEqual(resultat_fragile["lambda2_min_apres_suppression"], 0.0)
        self.assertEqual(robuste, robuste_initial)
        self.assertEqual(fragile, fragile_initial)


if __name__ == "__main__":
    unittest.main()