import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier



def charge_donnees():
    donnees = load_breast_cancer()
    X = donnees.data
    y = donnees.target

    X_train_complet, X_test, y_train_complet, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_complet, y_train_complet,
        test_size=0.2, random_state=42, stratify=y_train_complet
    )

    print("Entraînement :", X_train.shape)
    print("Validation :", X_val.shape)
    print("Test :", X_test.shape)

    return X_train_complet, X_test, y_train_complet, y_test, X_train, X_val, y_train, y_val


def etape2_arret_anticipe(X_train, X_val, y_train, y_val, X_test, y_test):
    modele = XGBClassifier(
        n_estimators=1000,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss",
        early_stopping_rounds=20
    )

    modele.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train), (X_val, y_val)],
        verbose=False
    )

    predictions = modele.predict(X_test)

    print("Exactitude test :", round(accuracy_score(y_test, predictions), 3))
    print("Meilleure itération :", modele.best_iteration)

    return modele, predictions


def exercice2_1(modele):
    print("Nombre d'arbres autorisés :", modele.n_estimators)
    print("Nombre d'arbres conservés :", modele.best_iteration + 1)


def exercice2_2(X_train, X_val, y_train, y_val):
    modele = XGBClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=4,
        random_state=42
    )

    try:
        modele.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            eval_metric="logloss",
            early_stopping_rounds=20,
            verbose=False
        )
    except TypeError as erreur:
        print("Erreur :", erreur)


def etape3_learning_rate(X_train, X_val, y_train, y_val, X_test, y_test):
    for taux in (0.2, 0.1, 0.05, 0.03, 0.01):
        modele = XGBClassifier(
            n_estimators=1000,
            learning_rate=taux,
            max_depth=4,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric="logloss",
            early_stopping_rounds=20
        )

        modele.fit(
            X_train, y_train,
            eval_set=[(X_train, y_train), (X_val, y_val)],
            verbose=False
        )

        predictions = modele.predict(X_test)
        exactitude = accuracy_score(y_test, predictions)

        print(
            f"learning_rate={taux} : "
            f"arbres utilisés={modele.best_iteration + 1}, "
            f"exactitude test={round(exactitude, 3)}"
        )


def etape4_courbe(modele, X_train, X_val, y_train, y_val):
    modele.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train), (X_val, y_val)],
        verbose=False
    )

    resultats = modele.evals_result()

    plt.figure(figsize=(8, 5))
    plt.plot(resultats["validation_0"]["logloss"], label="Entraînement")
    plt.plot(resultats["validation_1"]["logloss"], label="Validation")
    plt.axvline(
        modele.best_iteration,
        color="red",
        linestyle="--",
        label="Meilleure itération"
    )
    plt.xlabel("Nombre d'arbres")
    plt.ylabel("Logloss")
    plt.legend()
    plt.tight_layout()
    plt.show()


def etape5_comparaison(X_train_complet, y_train_complet, X_test, y_test, predictions):
    modele_sans_validation = XGBClassifier(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )

    modele_sans_validation.fit(X_train_complet, y_train_complet)

    predictions_sans = modele_sans_validation.predict(X_test)
    exactitude_sans = accuracy_score(y_test, predictions_sans)
    exactitude_avec = accuracy_score(y_test, predictions)

    print("Sans validation, 100 arbres fixes :", round(exactitude_sans, 3))
    print("Avec arrêt anticipé :", round(exactitude_avec, 3))
