# Journal des modifications

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).
Versions : [SemVer](https://semver.org/lang/fr/).

## [Non publié]

## [0.1.0] — 2026-09-15

### Ajouté

- Calculatrice de bureau Qt (PySide6) : addition, soustraction, multiplication,
  division, en arithmétique décimale exacte.
- Touches `C`, `CE`, `⌫`, `±`, séparateur décimal, répétition par `=`.
- Pilotage complet au clavier.
- Messages d'erreur pour la division par zéro et le dépassement de capacité.
- Suite de 105 tests (domaine, vue-modèle, interface) avec couverture à 100 %.
- Intégration continue GitHub Actions : format, lint, typage strict, tests sur
  Ubuntu / Windows / macOS et Python 3.11 / 3.12 / 3.13, construction du paquet.
- Crochets `pre-commit` reproduisant les contrôles de la CI.
- Documentation : architecture, guide d'utilisation, guide de développement,
  journal des décisions.

[Non publié]: https://github.com/alnews2/EvaluationDeDEVIN/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/alnews2/EvaluationDeDEVIN/releases/tag/v0.1.0
