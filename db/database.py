import sqlite3 # importation de la bibliothèque sqlite3
from icecream import ic


#connexion à la base de données (techcrunch.db) ou création si elle n'existe pas
def init_db(db_path = 'techcrunch.db'):
    conn = sqlite3.connect('db_path')
    cursor = conn.cursor()

    with open('db/schema.sql', 'r') as schema_file:
        schema = schema_file.read()
        cursor.executescript(schema)

    conn.commit()
    conn.close()
    ic("Base de données créée avec succès")


#fonction pour insérer les articles dans la base de données
def insert_article(article_data, db_path = 'techcrunch.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #nous insérons l' auteur de l'article dans la table categories s'il n'existe pas déjà.Ensuite, nous récupérons l'ID de l'auteur en utilisant son nom.

    cursor.execute(
    "INSERT OR IGNORE INTO authors (author_name) VALUES (?)", (article_data['Auteur'],))
    cursor.execute(
        "SELECT author_id FROM authors WHERE author_name = (?)", (article_data['Auteur'],))
    author_id = cursor.fetchone()[0]

    #nous insérons la catégorie de l'article dans la table categories s'il n'existe pas déjà.Ensuite, nous récupérons l'ID de la catégorie en utilisant son nom.
    cursor.exectute(
        "INSERT OR IGNORE INTO  categories (category_name, category_url) VALUES (?, ?)", (article_data['Categorie'], article_data['URl_categorie']))
    cursor.execute(
        "SELECT category_id FROM categories WHERE category_name = (?)", (article_data['Categorie'],))
    category_id = cursor.fetchone()[0]

    #inserer l'article et toutes les informations, y compris  les clés étrangères de l'autheur et de la catégorie
    cursor.execute(
        "INSERT OR IGNORE INTO articles (title,url, date_relative, date_absolute, author_id,category_id) VALUES (?,?,?,?,?,?)",
        (article_data['Title'],
        article_data['URL'],
        article_data['Date_relative'],
        article_data['Date_absolue'],
        author_id,
        category_id
        )
    )

# sauvegardons les modifications et fermons la connexion à la base de données.
    conn.commit()
    conn.close()