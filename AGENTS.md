# Consignes pour les agents

Dépôt d'une calculatrice de bureau Python / PySide6. Le commanditaire
n'intervient pas dans le code : la CI et les tests font foi.

## Commandes

```bash
uv venv --python 3.12 && uv pip install -e ".[dev]"   # installation
uv run ruff format . && uv run ruff check --fix .     # format + lint
uv run mypy                                           # typage strict
uv run pytest                                         # tests (couverture 100 % exigée)
uv run calculatrice                                   # lancement
```

Les tests d'interface tournent sans écran : `QT_QPA_PLATFORM=offscreen` est
positionné par `tests/conftest.py`.

## Règles

- `calculatrice.core` ne doit **jamais** importer PySide6.
- Toute nouvelle touche se déclare dans `KEY_SPECS`
  (`src/calculatrice/ui/main_window.py`), pas en câblant un widget à la main.
- La couverture doit rester à 100 % : `--cov-fail-under=100` est dans
  `pyproject.toml`.
- Mettre à jour `CHANGELOG.md`, et `docs/utilisation.md` si le comportement
  visible change ; ajouter une ADR dans `docs/decisions.md` pour tout choix
  structurant.
- Documentation, messages d'interface et docstrings en français ; identifiants
  de code en anglais.
