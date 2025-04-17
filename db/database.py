import sqlite3
from icecream import ic

#connexion à la base de données (techcrunch.db) ou création si elle n'existe pas
conn = sqlite3.connect('techcrunch.db')
cursor = conn.cursor()

with open('schema.sql', 'r') as schema_file:
    schema = schema_file.read()

    cursor.executescript(schema)

conn.commit()
conn.close()
ic("Base de données créée avec succès")

def insert_articles(article_data, db_path = 'techcrunch.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


cursor.execute(
    "INSERT OR IGNORE INTO authors (author_name) VALUES (?)", (article_data['Auteur'],)
    )