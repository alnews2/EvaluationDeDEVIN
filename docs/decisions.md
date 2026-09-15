# Journal des décisions d'architecture

Format court inspiré des *Architecture Decision Records* : une décision, son
contexte, ses conséquences. Les décisions ne sont jamais réécrites ; une
décision remplacée est marquée « remplacée par … ».

## ADR-001 — Python 3.11+ et PySide6

*Statut : accepté (v0.1.0).*

**Contexte.** Application de bureau devant évoluer par incréments, sans
intervention manuelle sur le code.

**Décision.** Python 3.11 minimum (syntaxe de typage moderne) et PySide6, les
bindings Qt 6 officiels sous licence LGPL.

**Conséquences.** Aucune contrainte de licence sur l'application (contrairement
à PyQt, en GPL). Le paquet PySide6 est volumineux (~150 Mo), ce qui est sans
importance pour un poste de travail.

## ADR-002 — Arithmétique décimale

*Statut : accepté (v0.1.0).*

**Contexte.** Une calculatrice qui afficherait `0.30000000000000004` pour
`0,1 + 0,2` serait considérée comme fausse par ses utilisateurs.

**Décision.** Tous les calculs utilisent `decimal.Decimal`, avec 28 chiffres
significatifs en interne et 12 à l'affichage.

**Conséquences.** Résultats exacts en base 10. Les dépassements de capacité
doivent être traités explicitement (`OverflowLimitError`).

## ADR-003 — Découpage MVVM et domaine sans Qt

*Statut : accepté (v0.1.0).*

**Contexte.** Les tests d'interface sont lents et fragiles ; le comportement
métier doit rester vérifiable instantanément.

**Décision.** Trois couches (`core`, `ui.view_model`, `ui.main_window`), avec
interdiction pour `core` d'importer PySide6.

**Conséquences.** La quasi-totalité des tests s'exécute sans interface. Le prix
à payer est une couche d'adaptation supplémentaire, qui reste mince.

## ADR-004 — Clavier décrit par une table déclarative

*Statut : accepté (v0.1.0).*

**Contexte.** Chaque évolution risque d'ajouter des touches ; le câblage manuel
de chaque bouton multiplierait les endroits à modifier.

**Décision.** Les touches sont décrites par `KEY_SPECS` (libellé, position,
action, raccourci, nom accessible) ; la fenêtre construit tout à partir de là.

**Conséquences.** Ajouter une touche = ajouter une ligne. Les tests parcourent
la table et couvrent donc automatiquement les nouvelles touches.

## ADR-005 — Couverture exigée à 100 %

*Statut : accepté (v0.1.0).*

**Contexte.** Le commanditaire ne relit pas le code : la CI est le seul filet.

**Décision.** Le seuil de couverture est fixé à 100 % (branches comprises), les
rares garde-fous défensifs étant marqués `# pragma: no cover`.

**Conséquences.** Toute ligne ajoutée sans test fait échouer la CI. Sur une base
de cette taille, le coût est négligeable et le signal est net.

## ADR-006 — Évaluation de gauche à droite

*Statut : accepté (v0.1.0).*

**Contexte.** `2 + 3 × 4` vaut `14` en notation mathématique, `20` sur une
calculatrice de bureau.

**Décision.** Comportement « calculatrice de bureau » : chaque opérateur valide
l'opération précédente.

**Conséquences.** Comportement conforme à l'attente pour ce type d'appareil et
documenté dans `docs/utilisation.md`. Une éventuelle priorité opératoire
nécessiterait une pile d'opérations et une nouvelle ADR.
