# Architecture

## Vue d'ensemble

L'application suit un découpage **MVVM** en trois couches strictement ordonnées :
chaque couche ne connaît que la précédente.

```
┌─────────────────────────────────────────────┐
│ calculatrice.ui.main_window  (Vue)          │  widgets Qt, clavier, style
│   • ne contient aucune règle de calcul      │
└───────────────┬─────────────────────────────┘
                │ signaux / appels
┌───────────────▼─────────────────────────────┐
│ calculatrice.ui.view_model  (Vue-modèle)    │  adapte le métier à Qt
│   • publie display_changed / error_state    │
└───────────────┬─────────────────────────────┘
                │
┌───────────────▼─────────────────────────────┐
│ calculatrice.core  (Domaine, sans Qt)       │  automate, opérations, formatage
│   • 100 % testable sans interface           │
└─────────────────────────────────────────────┘
```

**Règle d'or : `calculatrice.core` n'importe jamais PySide6.** C'est ce qui
permet de tester tout le comportement métier en quelques millisecondes, et de
remplacer un jour l'interface (web, ligne de commande) sans toucher au calcul.

## Modules

| Module | Responsabilité |
| --- | --- |
| `core/operations.py` | Les quatre opérations, en `Decimal`, et l'énumération `Operator`. |
| `core/formatting.py` | Mise en forme du nombre affiché (précision, notation scientifique). |
| `core/errors.py` | Erreurs métier portant un message déjà rédigé pour l'utilisateur. |
| `core/engine.py` | Automate : saisie, opération en attente, accumulateur, erreurs. |
| `ui/view_model.py` | `QObject` qui délègue à l'automate et publie l'état par signaux. |
| `ui/main_window.py` | Description déclarative du clavier (`KEY_SPECS`) et fenêtre. |
| `ui/styles.py` | Feuille de style Qt. |
| `app.py` | Point d'entrée : `QApplication`, fenêtre, boucle d'évènements. |

## L'automate de calcul

`CalculatorEngine` maintient quatre informations :

| État | Rôle |
| --- | --- |
| `_entry` | Saisie courante, sous forme de texte (c'est ce qui est affiché). |
| `_accumulator` | Résultat partiel, à gauche de l'opération en attente. |
| `_pending` | Opération en attente d'un second opérande. |
| `_entry_is_stale` | Vrai quand la prochaine saisie doit remplacer l'affichage. |

Deux états supplémentaires (`_repeat_operator`, `_repeat_operand`) permettent de
répéter la dernière opération lorsqu'on appuie plusieurs fois sur `=`.

Enchaînement typique de `2 + 3 × 4 =` :

| Touche | `_accumulator` | `_pending` | Affichage |
| --- | --- | --- | --- |
| `2` | — | — | `2` |
| `+` | `2` | `+` | `2` |
| `3` | `2` | `+` | `3` |
| `×` | `5` | `×` | `5` |
| `4` | `5` | `×` | `4` |
| `=` | `20` | — | `20` |

L'évaluation est donc **de gauche à droite**, sans priorité opératoire : c'est
le comportement attendu d'une calculatrice de bureau (et non d'un tableur).

### Gestion des erreurs

Une opération illicite lève une `CalculationError`, que l'automate convertit en
état d'erreur : l'affichage montre le message, et **toutes les touches sont
ignorées** jusqu'à `C` ou `CE`. Ce choix évite de calculer à partir d'un état
incohérent.

## Choix techniques

| Choix | Motif |
| --- | --- |
| **`decimal.Decimal`** | `0,1 + 0,2` doit afficher `0,3`. Les `float` binaires donneraient `0,30000000000000004`. |
| **PySide6** (et non PyQt) | Bindings officiels Qt, licence LGPL : aucune contrainte de licence sur l'application. |
| **Interface décrite en Python** (`KEY_SPECS`) et non en `.ui` | Ajouter une touche = ajouter une ligne dans une table ; le diff est lisible et testable. |
| **Vue-modèle intermédiaire** | Permet de tester la logique d'affichage (signaux, état d'erreur) sans widget. |
| **Noms d'objets Qt stables** (`button_add`, `display`) | Les tests d'interface s'appuient sur des identifiants, pas sur des positions. |
| **Couverture exigée à 100 %** | Sur une base de cette taille, toute ligne non couverte est un oubli, pas un arbitrage. |

## Évolutions prévues

Le découpage a été pensé pour que les évolutions restent locales :

| Évolution | Fichiers touchés |
| --- | --- |
| Nouvelle opération (pourcentage, racine…) | `core/operations.py` + une entrée dans `KEY_SPECS` |
| Historique des calculs | nouveau module `core/history.py` + un widget |
| Thème clair / sombre | `ui/styles.py` |
| Interface web ou ligne de commande | nouvelle couche vue, `core` inchangé |
