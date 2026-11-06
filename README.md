# RAG Assistant – Base de connaissances interne

## Contexte et objectif
Problème métier, utilisateurs cibles, valeur apportée.

## Démo
GIF / lien vers la démo en ligne.

## Architecture
Schéma : ingestion → chunking → embeddings → vector store → retrieval → LLM → réponse + sources.

## Stack technique
Python 3.11, [LLM], [modèle d'embeddings], [vector store], FastAPI, Streamlit, Docker.

## Installation
git clone ... / création de l'environnement / copie de .env.example

## Utilisation
1. Ingestion : `python -m src.ingestion --path data/raw`
2. Lancer l'API : `uvicorn src.api.main:app`
3. Lancer l'interface : `streamlit run app/main.py`

## Évaluation
Méthodologie, jeu de test, tableau de résultats (avant/après amélioration).

## Choix techniques et compromis
Pourquoi ce chunking, ce modèle, ce vector store.

## Sécurité et confidentialité
Gestion des secrets, données, prompt injection.

## Limites connues et pistes d'amélioration

## Licence