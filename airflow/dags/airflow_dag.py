from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
# Importer les modules avec les chemins corrects
from src.scrapper.main import scrape_techcrunch
from db.database import init_db, insert_article

# Ajouter le chemin du projet au PYTHONPATH pour trouver les modules
# Utiliser une variable d'environnement pour le chemin de base
BASE_DIR = os.environ.get('PROJECT_HOME', '/opt/airflow')
sys.path.append(BASE_DIR)



# Définir les arguments par défaut pour le DAG
default_arg = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 14),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=4),
}

# Définir le chemin de la base de données
DB_PATH = os.path.join(BASE_DIR, "dags", "techcrunch.db")

# Créer le DAG
dag = DAG(
    'techcrunch_scraper',
    default_args=default_arg,
    description='Scrape les derniers articles de Techcrunch',
    schedule=timedelta(days=1), #Executer tous les jours
)

# Fonction pour initialiser la base de données
def init_database():
    """
    Initialise la base de données SQLite avec le schéma défini.
    """
    init_db(DB_PATH)
    return "Base de données initialisée"

# Fonction pour scraper et stocker les articles
def scrape_and_store_articles():
    """
    Scrape les articles de TechCrunch et les stocke dans la base de données.
    Retourne le nombre d'articles traités.
    """
    articles = scrape_techcrunch()
    count = 0
    for article in articles:  # Correction: variable articles au singulier dans la boucle
        insert_article(article, DB_PATH)
        count += 1
    return f"{count} articles traités"

# Définir la tâche d'initialisation de la base de données
init_db_task = PythonOperator(
    task_id='init_database',
    python_callable=init_database,
    dag=dag,
)

# Définir la tâche de scraping et stockage
scrape_task = PythonOperator(
    task_id='scrape_techcrunch_articles',
    python_callable=scrape_and_store_articles,  # Utiliser la fonction correcte
    dag=dag,
)

# Définir l'ordre des tâches
init_db_task >> scrape_task