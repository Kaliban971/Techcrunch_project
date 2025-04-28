# Importations nécessaires
from fastapi import FastAPI, HTTPException # HTTPException pour gérer les erreurs (ex: article non trouvé)
import uvicorn
from pydantic import BaseModel # Pour définir la structure des données
from datetime import datetime # Pour gérer les dates
import sqlite3 # Pour interagir avec la base de données SQLite
import os # Pour construire le chemin vers la base de données

# --- Configuration ---

# Crée une instance de l'application FastAPI
# C'est notre "assistant bibliothécaire" principal
app = FastAPI(
    title="API TechCrunch Articles",
    description="Une API pour exposer les articles scrapés de TechCrunch stockés dans SQLite.",
    version="1.0.0"
)

# Définit le chemin vers le fichier de base de données SQLite
# On suppose que api.py est dans 'api/' et la db dans 'db/' au même niveau que 'api/'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'techcrunch.db')

# --- Modèle de Données (Le Catalogue) ---

# Définit la structure d'un article tel qu'il sera exposé par l'API
# C'est la "fiche" que l'API renverra
class ArticleResponse(BaseModel):
    """
    Modèle Pydantic représentant un article pour la réponse de l'API.
    """
    article_id: int # L'identifiant unique de l'article
    titre: str # Le titre de l'article
    url_article: str # L'URL de l'article original
    date_absolute: datetime | None # La date de publication (peut être None si non trouvée)
    auteur_nom: str | None # Le nom de l'auteur (peut être None)
    categorie_nom: str | None # Le nom de la catégorie (peut être None)
    categorie_url: str | None # L'URL de la catégorie (peut être None)

    # Configuration pour permettre à Pydantic de lire les données depuis des objets (comme les tuples de SQLite)
    class Config:
        orm_mode = True # Ancienne syntaxe pour Pydantic v1, ou `from_attributes = True` pour Pydantic v2+

# --- Fonctions d'Accès à la Base de Données ---

def get_db_connection():
    """
    Établit et retourne une connexion à la base de données SQLite.
    Configure la connexion pour retourner les lignes comme des dictionnaires.
    """
    # Vérifie si le fichier de base de données existe
    if not os.path.exists(DATABASE_PATH):
        # Si la base n'existe pas, on lève une erreur claire
        raise HTTPException(status_code=500, detail=f"Erreur: La base de données '{DATABASE_PATH}' n'a pas été trouvée.")
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(DATABASE_PATH)
        # Permet d'accéder aux colonnes par leur nom (comme un dictionnaire)
        conn.row_factory = sqlite3.Row
        # Retourne l'objet de connexion
        return conn
    except sqlite3.Error as e:
        # Si la connexion échoue pour une autre raison
        raise HTTPException(status_code=500, detail=f"Erreur de connexion à la base de données: {e}")


# --- Points d'Accès (Les Guichets de l'API) ---

@app.get("/")
async def index():
    """
    Point d'accès racine. Retourne un message de bienvenue.
    C'est la page d'accueil de notre "bibliothèque" API.
    """
    # Retourne un simple message JSON
    return {"message": "Bienvenue sur l'API des articles TechCrunch!"}

@app.get("/articles", response_model=list[ArticleResponse])
async def get_all_articles(skip: int = 0, limit: int = 20):
    """
    Récupère une liste paginée de tous les articles de la base de données.
    Permet de demander une "page" d'articles (ex: les 20 premiers, puis les 20 suivants).

    Args:
        skip (int): Nombre d'articles à sauter (pour la pagination). Défaut 0.
        limit (int): Nombre maximum d'articles à retourner. Défaut 20.

    Returns:
        list[ArticleResponse]: Une liste d'objets articles.
    """
    # Requête SQL pour sélectionner les informations nécessaires en joignant les tables
    # On joint 'articles' avec 'authors' et 'categories' pour récupérer les noms
    query = """
        SELECT
            a.article_id,
            a.titre,
            a.url_article,
            a.date_absolute,
            au.author_name AS auteur_nom,
            c.category_name AS categorie_nom,
            c.category_url
        FROM articles a
        LEFT JOIN authors au ON a.author_id = au.author_id
        LEFT JOIN categories c ON a.category_id = c.category_id
        ORDER BY a.date_absolute DESC -- Trie par date la plus récente d'abord
        LIMIT ? OFFSET ? -- Applique la pagination
    """
    # Ouvre une connexion à la base de données
    conn = get_db_connection()
    # Crée un curseur pour exécuter la requête
    cursor = conn.cursor()
    try:
        # Exécute la requête SQL avec les paramètres de pagination
        cursor.execute(query, (limit, skip))
        # Récupère tous les résultats
        articles_db = cursor.fetchall()
    except sqlite3.Error as e:
        # Gère les erreurs SQL potentielles
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des articles: {e}")
    finally:
        # Ferme la connexion, que la requête ait réussi ou échoué
        conn.close()

    # Si aucun article n'est trouvé (peut arriver avec skip/limit)
    if not articles_db:
        # Retourne une liste vide, ce n'est pas une erreur en soi
        return []

    # Convertit les résultats de la base de données en objets ArticleResponse
    # Pydantic valide que les données correspondent au modèle défini
    # return [ArticleResponse.from_orm(article) for article in articles_db] # Pydantic v1
    return [ArticleResponse.model_validate(article) for article in articles_db] # Pydantic v2+


@app.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article_by_id(article_id: int):
    """
    Récupère un article spécifique par son ID.
    C'est comme demander un livre précis par son numéro de catalogue.

    Args:
        article_id (int): L'ID de l'article à récupérer.

    Returns:
        ArticleResponse: L'objet article correspondant à l'ID.

    Raises:
        HTTPException: Avec le code 404 si l'article n'est pas trouvé.
                       Avec le code 500 en cas d'erreur base de données.
    """
    # Requête SQL similaire à get_all_articles mais filtrée par article_id
    query = """
        SELECT
            a.article_id,
            a.titre,
            a.url_article,
            a.date_absolute,
            au.author_name AS auteur_nom,
            c.category_name AS categorie_nom,
            c.category_url
        FROM articles a
        LEFT JOIN authors au ON a.author_id = au.author_id
        LEFT JOIN categories c ON a.category_id = c.category_id
        WHERE a.article_id = ? -- Filtre par l'ID fourni
    """
    # Ouvre une connexion
    conn = get_db_connection()
    # Crée un curseur
    cursor = conn.cursor()
    try:
        # Exécute la requête avec l'ID de l'article
        cursor.execute(query, (article_id,))
        # Récupère un seul résultat (fetchone)
        article_db = cursor.fetchone()
    except sqlite3.Error as e:
        # Gère les erreurs SQL
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'article {article_id}: {e}")
    finally:
        # Ferme la connexion
        conn.close()

    # Si aucun article n'est trouvé avec cet ID
    if article_db is None:
        # Lève une erreur 404 (Not Found)
        raise HTTPException(status_code=404, detail=f"Article avec ID {article_id} non trouvé")

    # Convertit le résultat en objet ArticleResponse et le retourne
    # return ArticleResponse.from_orm(article_db) # Pydantic v1
    return ArticleResponse.model_validate(article_db) # Pydantic v2+


# --- Démarrage de l'API (Seulement si le script est exécuté directement) ---

# Cette partie permet de lancer le serveur FastAPI directement en exécutant `python api/api.py`
if __name__ == "__main__":
    # Lance le serveur Uvicorn
    # host="0.0.0.0" le rend accessible depuis d'autres machines sur le réseau
    # port=8000 est le port standard pour le développement
    # reload=True redémarre le serveur automatiquement si tu modifies le code (très pratique!)
    print(f"Vérification de la base de données à l'emplacement : {DATABASE_PATH}")
    if not os.path.exists(DATABASE_PATH):
        print(f"ERREUR: Le fichier de base de données '{DATABASE_PATH}' n'existe pas.")
        print("Assurez-vous que la base de données a été créée (par exemple avec Airflow ou db/database.py).")
    else:
        print(f"Base de données trouvée. Démarrage du serveur Uvicorn sur http://127.0.0.1:8000")
        uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)