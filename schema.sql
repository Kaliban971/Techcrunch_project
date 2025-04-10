-- Table Categories
CREATE TABLE categories (
    category_id INT PRIMARY KEY, AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL,
    category_url VARCHAR(255) NOT NULL,
    UNIQUE KEY (category_name)
);

-- Table Authors
CREATE TABLE authors (
    author_id INT PRIMARY KEY AUTO_INCREMENT,
    author_name VARCHAR(100) NOT NULL,
    UNIQUE KEY (author_name)
);

-- Table Articles
CREATE TABLE articles (
    article_id INT PRIMARY KEY AUTO_INCREMENT,
    titre VARCHAR(255) NOT NULL,
    url_article VARCHAR(255) NOT NULL,
    date_relative VARCHAR(50),
    date_absolute  DATETIME,
    author_id INT,
    category_id INT,
);