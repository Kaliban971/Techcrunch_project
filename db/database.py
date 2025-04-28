import sqlite3 # importation de la bibliothèque sqlite3
import json    # <-- NOUVEAU: On importe la bibliothèque pour travailler avec les fichiers JSON
from icecream import ic

# Fonction pour initialiser la base de données
# Crée la connexion, exécute le schéma SQL pour créer les tables si elles n'existent pas.
def init_db(db_path = 'techcrunch.db'):
    # Connexion à la base de données SQLite spécifiée par db_path
    conn = sqlite3.connect(db_path)
    # Création d'un objet curseur pour exécuter des commandes SQL
    cursor = conn.cursor()

    # Ouverture du fichier contenant le schéma SQL en mode lecture ('r')
    # 'with open' garantit que le fichier sera fermé même en cas d'erreur
    with open('db/schema.sql', 'r', encoding='utf-8') as schema_file: # Ajout de encoding='utf-8' pour la compatibilité
        # Lecture du contenu complet du fichier de schéma
        schema = schema_file.read()
        # Exécution du script SQL contenu dans la variable schema
        cursor.executescript(schema)

    # Sauvegarde (commit) des modifications apportées à la base de données
    conn.commit()
    # Fermeture de la connexion à la base de données
    conn.close()
    # Affichage d'un message de succès via icecream pour le débogage
    ic("Base de données initialisée ou déjà existante.")

# Fonction pour insérer les données d'un article dans la base de données
# Prend un dictionnaire 'article_data' et le chemin de la DB en entrée.
def insert_article(article_data, db_path = 'techcrunch.db'):
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    # Création d'un curseur pour exécuter les requêtes SQL
    cursor = conn.cursor()

    try: # <-- AJOUT: Bloc try pour gérer les erreurs potentielles (ex: données manquantes)
        # --- Insertion ou récupération de l'auteur ---
        # Essaye d'insérer l'auteur. S'il existe déjà, IGNORE ne fait rien.
        cursor.execute(
            "INSERT OR IGNORE INTO authors (author_name) VALUES (?)",
            (article_data['Auteur'],) # Assure-toi que la clé 'Auteur' existe dans tes données JSON
        )
        # Récupère l'ID de l'auteur
        cursor.execute(
            "SELECT author_id FROM authors WHERE author_name = (?)",
            (article_data['Auteur'],)
        )
        author_result = cursor.fetchone() # Récupère le résultat
        if author_result: # Vérifie si un auteur a été trouvé/inséré
             author_id = author_result[0]
             ic("Auteur trouvé/inséré:", article_data['Auteur'], "avec ID:", author_id)
        else:
             ic("ERREUR: Impossible de trouver/insérer l'auteur:", article_data.get('Auteur', 'Nom Manquant'))
             return # <-- AJOUT: Sortir si l'auteur n'est pas trouvé/inséré

        # --- Insertion ou récupération de la catégorie ---
        # Essaye d'insérer la catégorie. IGNORE si elle existe déjà.
        cursor.execute(
            "INSERT OR IGNORE INTO categories (category_name, category_url) VALUES (?, ?)",
            (article_data['Categorie'], article_data['URL_Categorie']) # Assure-toi que ces clés existent
        )
        # Récupère l'ID de la catégorie
        cursor.execute(
            "SELECT category_id FROM categories WHERE category_name = (?)",
            (article_data['Categorie'],)
        )
        category_result = cursor.fetchone() # Récupère le résultat
        if category_result: # Vérifie si une catégorie a été trouvée/insérée
            category_id = category_result[0]
            ic("Catégorie trouvée/insérée:", article_data['Categorie'], "avec ID:", category_id)
        else:
            ic("ERREUR: Impossible de trouver/insérer la catégorie:", article_data.get('Categorie', 'Nom Manquant'))
            return # <-- AJOUT: Sortir si la catégorie n'est pas trouvée/insérée

        # --- Insertion de l'article ---
        # Essaye d'insérer l'article complet. IGNORE si une URL identique existe déjà.
        cursor.execute(
            "INSERT OR IGNORE INTO articles (titre, url_article, date_relative, date_absolute, author_id, category_id) VALUES (?,?,?,?,?,?)",
            (article_data['Titre'],          # Assure-toi que 'Titre' existe
             article_data['URL_Article'],    # Assure-toi que 'URL_Article' existe
             article_data['Date_relative'],  # Assure-toi que 'Date_relative' existe
             article_data['Date_absolue'],   # Assure-toi que 'Date_absolue' existe
             author_id,
             category_id
            )
        )
        # rowcount > 0 signifie qu'une ligne a été insérée (et non ignorée)
        if cursor.rowcount > 0:
            ic("Article inséré:", article_data['Titre'])
        else:
            ic("Article déjà existant (ignoré):", article_data['Titre'])

        # Sauvegarde des modifications dans la base de données
        conn.commit()

    except KeyError as e: # <-- AJOUT: Gérer le cas où une clé attendue manque dans le JSON
        ic(f"ERREUR: Clé manquante dans les données de l'article: {e}")
        ic("Données de l'article problématique:", article_data)
    except Exception as e: # <-- AJOUT: Gérer d'autres erreurs potentielles
        ic(f"ERREUR inattendue lors de l'insertion de l'article: {e}")
        ic("Données de l'article problématique:", article_data)
        conn.rollback() # Annuler les changements pour cet article en cas d'erreur grave
    finally: # <-- AJOUT: Assurer la fermeture de la connexion quoi qu'il arrive
        # Fermeture de la connexion à la base de données
        conn.close()

# --- Bloc principal d'exécution ---
if __name__ == "__main__":
    # Étape 1: Initialiser la base de données (créer/vérifier les tables)
    db_file = 'techcrunch.db' # Nom du fichier de base de données
    init_db(db_file)

    # Étape 2: Définir le chemin vers le fichier JSON contenant les articles
    # Utilise un chemin relatif depuis la racine du projet
    json_file_path = 'profil.json'
    ic(f"Lecture des articles depuis: {json_file_path}")

    try:
        # Étape 3: Ouvrir et lire le fichier JSON
        # 'with open' s'assure que le fichier est bien fermé après lecture
        # encoding='utf-8' est important pour gérer les caractères spéciaux
        with open(json_file_path, 'r', encoding='utf-8') as f:
            # Charger les données JSON depuis le fichier dans une liste Python de dictionnaires
            articles_data = json.load(f)
            ic(f"Trouvé {len(articles_data)} articles dans le fichier JSON.")

        # Étape 4: Boucler sur chaque article chargé depuis le JSON
        # Pour chaque 'article' (qui est un dictionnaire) dans la liste 'articles_data'...
        for article in articles_data:
            # ...appeler la fonction insert_article pour l'insérer dans la base de données
            ic(f"Traitement de l'article: {article.get('Titre', 'Titre Manquant')}") # Affiche le titre pour suivre la progression
            insert_article(article, db_file) # On passe le dictionnaire de l'article et le nom du fichier DB

        # Étape 5: Afficher un message final une fois tous les articles traités
        ic("✅ Traitement de tous les articles terminé.")

    except FileNotFoundError: # Gérer le cas où le fichier JSON n'est pas trouvé
        ic(f"ERREUR: Le fichier JSON '{json_file_path}' n'a pas été trouvé. Vérifie le chemin.")
    except json.JSONDecodeError: # Gérer le cas où le JSON est mal formé
        ic(f"ERREUR: Le fichier JSON '{json_file_path}' n'est pas valide. Vérifie sa structure.")
    except Exception as e: # Gérer toute autre erreur imprévue
        ic(f"ERREUR inattendue lors de la lecture ou du traitement du JSON: {e}")