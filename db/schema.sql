--Sqlite3 schema for the project


-- Table Categories
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL,
    category_url TEXT NOT NULL,
    UNIQUE (category_name)
);

-- Table Authors
CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT NOT NULL,
    UNIQUE (author_name)
);

-- Table Articles
CREATE TABLE articles (
    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    url_article TEXT NOT NULL UNIQUE, -- Ajout de la colonne url_article et verifier que les url sont unique
    date_relative TEXT,
    date_absolute  DATETIME, -- Ajout de la colonne date_absolute stocker la date de publication de l'article
    author_id INTEGER,
    category_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Enregistre automatiquement quand l'article a été ajouté à la base,  DEFAULT CURRENT_TIMESTAMP = utilise l'heure actuelle par défaut
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, --Se met à jour automatiquement chaque fois que l'article est modifié
    FOREIGN KEY (author_id) REFERENCES authors(author_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );

