# Guide d'utilisation

## Lancement

```bash
uv run calculatrice     # environnement géré par uv
python -m calculatrice  # environnement Python courant
```

## Le clavier

```
┌──────┬──────┬──────┬──────┐
│  C   │  CE  │  ⌫   │  ÷   │
├──────┼──────┼──────┼──────┤
│  7   │  8   │  9   │  ×   │
├──────┼──────┼──────┼──────┤
│  4   │  5   │  6   │  −   │
├──────┼──────┼──────┼──────┤
│  1   │  2   │  3   │  +   │
├──────┼──────┼──────┼──────┤
│  ±   │  0   │  ,   │  =   │
└──────┴──────┴──────┴──────┘
```

| Touche | Rôle | Raccourci clavier |
| --- | --- | --- |
| `0`–`9` | Saisie d'un chiffre (15 au maximum) | `0`–`9` |
| `,` | Séparateur décimal, une seule fois par nombre | `,` ou `.` |
| `±` | Change le signe de la saisie | `F9` |
| `⌫` | Efface le dernier caractère saisi | `Retour arrière` |
| `CE` | Efface la saisie en cours, conserve l'opération en attente | `Suppr` |
| `C` | Remet tout à zéro | `Échap` |
| `+ − × ÷` | Opérations | `+` `-` `*` `/` |
| `=` | Calcule le résultat | `Entrée` ou `=` |

## Comportements à connaître

**Évaluation de gauche à droite.** `2 + 3 × 4 =` affiche `20` : chaque opérateur
valide l'opération précédente, comme sur une calculatrice de bureau. Il n'y a
pas de priorité de la multiplication (ce serait `14`).

**Résultats intermédiaires.** Appuyer sur un opérateur affiche immédiatement le
résultat partiel : `2 + 3 ×` affiche `5`.

**Répétition avec `=`.** Après `2 + 3 =` (soit `5`), chaque `=` supplémentaire
rejoue la dernière opération : `8`, puis `11`.

**Correction d'opérateur.** Deux opérateurs successifs : c'est le dernier qui
compte. `8 + − 2 =` donne `6`.

**Chaînage sur un résultat.** Après un résultat, un opérateur repart de ce
résultat ; un chiffre commence au contraire un nouveau calcul.

**Précision.** Les calculs sont exacts en base 10 : `0,1 + 0,2` affiche bien
`0,3`. L'afficheur conserve 12 chiffres significatifs, et bascule en notation
scientifique (`1.5e+20`) au-delà.

## Messages d'erreur

| Message | Cause | Sortie |
| --- | --- | --- |
| `Division par zéro` | Division dont le diviseur vaut zéro | `C` ou `CE` |
| `Résultat hors limites` | Résultat trop grand pour être représenté | `C` ou `CE` |

Tant qu'un message est affiché, les autres touches sont **volontairement
ignorées** : impossible de poursuivre un calcul à partir d'un état invalide.
