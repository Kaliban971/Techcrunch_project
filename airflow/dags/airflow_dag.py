import re
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.scrapper.main import scrape_techcrunch
from src.db.database import init_db, insert_article


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

# Créer le DAG
dag = DAG(
    'techcrunch_scraper',
    default_args=default_arg,
    description='Scrape les derniers articles de Techcrunch',
    schedule=timedelta(days=1), #Executer tous les jours
)

# Fonction pour initialiser la base de données
def init_database():
    init_db("/opt/airflow/dags/techcrunch.db")


def scrape_and_store_article():
    articles = scrape_techcrunch()
    for articles in articles:
        insert_article(articles, "/opt/airflow/dags/techcrunch.db")
    return len(articles)


# Définir la tâche d'initialisation de la base de données
init_db_task = PythonOperator(
    task_id='init_database',
    python_callable=init_database,
    dag=dag,
)



# Définir la tâche de scraping et stockage
scrape_task = PythonOperator(
    task_id='scrape_techcrunch_articles',
    python_callable=scrape_techcrunch,
    dag=dag,
)

# definir l'ordre des tâches
init_db_task >> scrape_task


#NOTE:Imported the scrape_techcrunch function from main.py
#NOTE Set up a basic DAG with default arguments
#NOTE Created a PythonOperator task that calls the scrape_techcrunch function
#NOTE Added the ability to specify the output file path
#TODO:Finir la compréension du code de airflow