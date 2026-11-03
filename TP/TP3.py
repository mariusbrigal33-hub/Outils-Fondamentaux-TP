import pandas as pd
import warnings
import xgboost as xgb

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, recall_score


def charge_donnees():
    donnees = load_breast_cancer()
    X = pd.DataFrame(donnees.data, columns=donnees.feature_names)
    y = pd.Series(donnees.target, name="target")

    print(X.shape)
    print(dict(zip([0, 1], donnees.target_names)))
    print(y.value_counts())

    return X, y, donnees


def separe_donnees(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    print(X_train.shape, X_test.shape)
    print(y_train.value_counts(normalize=True).round(3))
    print(y_test.value_counts(normalize=True).round(3))

    return X_train, X_test, y_train, y_test


def exercice2_1(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Sans stratification :")
    print(y_test.value_counts(normalize=True).round(3))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    print("Avec stratification :")
    print(y_test.value_counts(normalize=True).round(3))


def arbre_decision(X_train, X_test, y_train, y_test):
    arbre = DecisionTreeClassifier(max_depth=4, random_state=42)
    arbre.fit(X_train, y_train)

    pred_arbre = arbre.predict(X_test)

    print("Exactitude test :", round(accuracy_score(y_test, pred_arbre), 3))
    print(confusion_matrix(y_test, pred_arbre))

    return arbre, pred_arbre


def exercice3_1(X_train, X_test, y_train, y_test):
    arbre = DecisionTreeClassifier(random_state=42)
    arbre.fit(X_train, y_train)

    pred_train = arbre.predict(X_train)
    pred_test = arbre.predict(X_test)

    print("Exactitude entraînement :", round(accuracy_score(y_train, pred_train), 3))
    print("Exactitude test :", round(accuracy_score(y_test, pred_test), 3))


def foret_aleatoire(X_train, X_test, y_train, y_test, X):
    foret = RandomForestClassifier(n_estimators=200, random_state=42)
    foret.fit(X_train, y_train)

    pred_foret = foret.predict(X_test)

    print("Exactitude test :", round(accuracy_score(y_test, pred_foret), 3))

    importances = pd.Series(
        foret.feature_importances_, index=X.columns
    ).sort_values(ascending=False)

    print(importances.head(5))

    return foret, pred_foret


def exercice4_1(arbre, foret, X_test, y_test):
    pred_arbre = arbre.predict(X_test)
    pred_foret = foret.predict(X_test)

    print("Exactitude arbre :", round(accuracy_score(y_test, pred_arbre), 3))
    print("Exactitude forêt :", round(accuracy_score(y_test, pred_foret), 3))


def modele_xgboost(X_train, X_test, y_train, y_test):
    modele = xgb.XGBClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=3,
        random_state=42,
        eval_metric="logloss"
    )

    modele.fit(X_train, y_train)
    pred_xgb = modele.predict(X_test)

    print("Exactitude test :", round(accuracy_score(y_test, pred_xgb), 3))

    return modele


def test_avertissement():
    with warnings.catch_warnings(record=True) as enregistrees:
        warnings.simplefilter("always")
        xgb.XGBClassifier(use_label_encoder=True, eval_metric="logloss")

        for w in enregistrees:
            print(w.category.__name__, ":", w.message)


def exercice5_1(X_train, X_test, y_train, y_test):
    for taux in [0.01, 0.1, 0.3]:
        modele = xgb.XGBClassifier(
            n_estimators=200,
            learning_rate=taux,
            max_depth=3,
            random_state=42,
            eval_metric="logloss"
        )

        modele.fit(X_train, y_train)
        prediction = modele.predict(X_test)

        print("Learning rate :", taux)
        print("Exactitude :", round(accuracy_score(y_test, prediction), 3))


def compare_metriques(y_test, pred_arbre, donnees):
    print(classification_report(
        y_test, pred_arbre, target_names=donnees.target_names
    ))


def exercice6_1(y_test, pred_arbre):
    print("Rappel classe 1 :", round(recall_score(y_test, pred_arbre), 3))
    print("Rappel classe 0 :", round(recall_score(y_test, pred_arbre, pos_label=0), 3))