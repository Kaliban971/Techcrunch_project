# Projet de Scraping TechCrunch

## Description
Ce projet est un outil de scraping qui extrait des articles du site TechCrunch et les stocke dans une base de données. Il utilise Python avec les bibliothèques Parsel et Requests pour extraire les données, et est conçu pour être utilisé dans un contexte de data engineering.

## Fonctionnalités actuelles
- Extraction des articles de la page d'accueil de TechCrunch
- Récupération des informations suivantes pour chaque article :
  - Catégorie
  - URL de la catégorie
  - URL de l'article
  - Titre
  - Auteur
  - Date relative (ex: "24 minutes ago")
  - Date absolue (format ISO)
  - Contenu complet de l'article
- Stockage des données au format JSON

## Structure du projet
- `main.py` : Script principal de scraping
- `schema.sql` : Schéma de la base de données pour stocker les articles
- `profil.json` : Fichier de sortie contenant les articles scrapés
- `pyproject.toml` : Configuration du projet et dépendances

## Prérequis
- Python 3.12 ou supérieur
- Dépendances listées dans `pyproject.toml`

## Installation
```bash
# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
# Sur Windows
.venv\Scripts\activate

# Installer les dépendances
pip install -e .
```

## Utilisation
```bash
python main.py
```

## Améliorations à implémenter (Test technique Data Engineer)

### 1. Pipeline ETL complet
- **Extract** : Améliorer le scraping pour gérer la pagination et récupérer plus d'articles
- **Transform** : Nettoyer et structurer les données (dates, textes, etc.)
- **Load** : Implémenter le chargement des données dans une base de données SQL

### 2. Base de données
- Implémenter le schéma SQL défini dans `schema.sql`
- Ajouter des fonctions pour insérer, mettre à jour et interroger les données
- Gérer les doublons et les mises à jour d'articles existants

### 3. Automatisation et planification
- Mettre en place un système de planification (cron, Airflow, etc.)
- Exécuter le scraping à intervalles réguliers
- Journaliser les exécutions et gérer les erreurs

### 4. Analyse des données
- Implémenter des requêtes d'analyse sur les articles collectés
- Créer des visualisations des tendances (articles par catégorie, par auteur, etc.)
- Extraire des insights à partir du contenu des articles

### 5. API REST
- Développer une API pour accéder aux données collectées
- Implémenter des endpoints pour rechercher et filtrer les articles
- Documenter l'API avec Swagger/OpenAPI

### 6. Tests et monitoring
- Ajouter des tests unitaires et d'intégration
- Mettre en place un système de monitoring pour suivre les performances
- Alertes en cas d'échec du scraping ou de problèmes de données

## Bonnes pratiques à suivre
- Respecter les règles d'éthique du scraping (robots.txt, délais entre requêtes)
- Documenter le code et les fonctionnalités
- Utiliser des patterns de conception appropriés
- Gérer efficacement les erreurs et les cas limites