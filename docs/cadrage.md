# Cadrage du projet

## 1. Contexte et problème
Les collaborateurs perdent du temps à chercher des informations RH
(congés, télétravail, arrêts maladie, période d'essai…) dispersées
dans de nombreux documents. Les mêmes questions reviennent au service RH.

## 2. Utilisateurs cibles
- **Salariés** : posent des questions pratiques en langage naturel.
- **Équipe RH** : réduit le volume de questions répétitives.
- **Administrateur** (moi) : ajoute des documents et surveille la qualité.

## 3. Périmètre
**Dans le périmètre** : questions sur les documents RH indexés
(droits, procédures, démarches), en français.
**Hors périmètre** : avis juridique personnalisé, données personnelles
d'un salarié (solde de congés, paie), questions non RH.

## 4. Fonctionnalités attendues
- Répondre en français à partir des documents uniquement.
- Citer les sources (document et page).
- Refuser de répondre quand l'information est absente.
- Interface web simple et API.

## 5. Questions types (à compléter, 10 à 15)
| # | Question | Document source attendu | Type |
|---|----------|-------------------------|------|
| 1 | Comment sont acquis les congés payés ? | | Dans le corpus |
| 2 | Quelles sont les règles du télétravail ? | | Dans le corpus |
| 3 | Que faire en cas d'arrêt maladie ? | | Dans le corpus |
| 4 | Quelle est la durée de la période d'essai ? | | Dans le corpus |
| 5 | Comment fonctionne la rupture conventionnelle ? | | Dans le corpus |
| 6 | Comment sont payées les heures supplémentaires ? | | Dans le corpus |
| 7 | Quelles données personnelles un employeur peut-il collecter ? | | Dans le corpus |
| 8 | Quel est mon solde de congés ? | aucun | Hors périmètre (refus) |
| 9 | Quelle est la recette de la ratatouille ? | aucun | Hors périmètre (refus) |
| 10 | Quelle est la capitale de l'Australie ? | aucun | Hors périmètre (refus) |

## 6. Critères de succès (mesurables)
| Critère | Cible |
|---------|-------|
| Document source correct dans le top 5 (recall@5) | ≥ 85 % |
| Réponses fidèles au contexte (pas d'invention) | ≥ 90 % |
| Refus correct sur les questions hors périmètre | 100 % |
| Réponses avec au moins une source citée | 100 % |
| Temps de réponse | < 10 s |

## 7. Contraintes
- **RGPD** : aucune donnée personnelle réelle dans le corpus ni les logs.
- **Langue** : français (modèle d'embeddings multilingue).
- **Coûts** : suivi des tokens par requête, budget maximal à fixer.
- **Sécurité** : clés API hors du dépôt, protection contre le prompt injection.

## 8. Hypothèses et risques
- Documents publics, donc pas de confidentialité à gérer.
- Risque : PDF scannés ou à mise en page complexe, qui dégradent l'extraction.
- Risque : textes juridiques qui évoluent, donc réponses potentiellement obsolètes.

## 9. Livrables
Dépôt GitHub, README, démo en ligne, rapport d'évaluation.