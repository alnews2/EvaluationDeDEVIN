# Guide de développement

## Environnement

```bash
uv venv --python 3.12
uv pip install -e ".[dev]"
uv run pre-commit install
```

`uv` n'est pas obligatoire : `python -m venv .venv` puis `pip install -e ".[dev]"`
donne le même résultat. Toutes les commandes ci-dessous fonctionnent avec ou
sans le préfixe `uv run`.

## Boucle de vérification

| Commande | Vérifie |
| --- | --- |
| `ruff format .` | Formatage automatique |
| `ruff check --fix .` | Lint (imports, docstrings, annotations, pièges courants) |
| `mypy` | Typage strict, sur le code **et** les tests |
| `pytest` | 105 tests, couverture exigée à 100 % |

Ces quatre commandes sont exactement celles exécutées par la CI et par
`pre-commit` : ce qui passe en local passe en CI.

## Organisation des tests

| Fichier | Portée |
| --- | --- |
| `tests/test_operations.py` | Les quatre opérations, erreurs comprises |
| `tests/test_formatting.py` | Mise en forme de l'afficheur |
| `tests/test_engine.py` | Automate complet, via une mini-syntaxe de séquences |
| `tests/test_view_model.py` | Émission des signaux Qt |
| `tests/test_main_window.py` | Interface réelle : clics souris et raccourcis clavier |
| `tests/test_app.py` | Point d'entrée |

Les tests d'interface utilisent `pytest-qt` et s'exécutent **sans écran** grâce
à `QT_QPA_PLATFORM=offscreen` (positionné par `tests/conftest.py`).

La syntaxe de séquence utilisée dans `test_engine.py` rend les cas lisibles :

```python
assert press(engine, "2+3*4=") == "20"
```

## Intégration continue

`.github/workflows/ci.yml` définit trois tâches :

1. **Qualité** — `ruff format --check`, `ruff check`, `mypy` (Ubuntu, Python 3.12).
2. **Tests** — matrice Ubuntu / Windows / macOS × Python 3.11 / 3.12 / 3.13,
   avec installation des bibliothèques Qt nécessaires sous Linux.
3. **Paquet** — `uv build`, puis installation du wheel produit pour vérifier
   qu'il est utilisable ; les artefacts sont publiés sur la CI.

Dependabot (`.github/dependabot.yml`) propose chaque semaine les mises à jour
de dépendances et chaque mois celles des actions GitHub.

## Ajouter une fonctionnalité

Exemple : ajouter une touche « pourcentage ».

1. **Domaine d'abord** : implémenter le calcul dans `core/`, et écrire le test
   correspondant dans `tests/test_engine.py`.
2. **Vue-modèle** : exposer une méthode qui délègue à l'automate.
3. **Interface** : ajouter une entrée dans `KEY_SPECS`
   (`src/calculatrice/ui/main_window.py`) — nom, libellé, position, action,
   raccourci. Rien d'autre à câbler : la fenêtre construit le clavier à partir
   de cette table, et `test_window_exposes_every_declared_key` couvre
   automatiquement la nouvelle touche.
4. **Documentation** : mettre à jour `docs/utilisation.md` et `CHANGELOG.md`.

## Conventions

- Le domaine (`calculatrice.core`) n'importe jamais PySide6.
- Toute fonction publique est annotée et documentée (contrôlé par `ruff`/`mypy`).
- Les messages destinés à l'utilisateur sont rédigés dans les erreurs métier,
  jamais dans la couche graphique.
- Les identifiants Qt (`objectName`) sont stables : les tests s'y réfèrent.
