# Contribuer

## Avant de commencer

```bash
uv venv --python 3.12
uv pip install -e ".[dev]"
uv run pre-commit install
```

Le détail de l'environnement, des tests et de la CI se trouve dans
[docs/developpement.md](docs/developpement.md).

## Règles

1. **Le domaine avant l'interface** : une règle de calcul s'implémente dans
   `calculatrice.core`, jamais dans un widget.
2. **Tout ajout est testé** : la couverture exigée est de 100 %.
3. **Les quatre contrôles doivent passer** avant toute demande de fusion :
   `ruff format --check .`, `ruff check .`, `mypy`, `pytest`.
4. **Documentation à jour** : `CHANGELOG.md` systématiquement,
   `docs/utilisation.md` si le comportement visible change, et une nouvelle
   entrée dans `docs/decisions.md` pour tout choix structurant.

## Messages de commit

Convention [Conventional Commits](https://www.conventionalcommits.org/fr/) :

```
feat(ui): ajouter la touche pourcentage
fix(core): corriger l'arrondi des divisions périodiques
docs: préciser le comportement de la touche CE
```

## Demandes de fusion

Une demande de fusion décrit *pourquoi* le changement est fait, pas seulement
*ce qui* change. La CI doit être verte : elle est bloquante.
