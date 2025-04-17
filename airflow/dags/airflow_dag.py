from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.scrapper.main import scrape_techcrunch

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

# Définir la tâche de scraping
scrape_task = PythonOperator(
    task_id='scrape_techcrunch_articles',
    python_callable=scrape_techcrunch,
    op_kwargs={'output_file':'/opt/airflow/dags/techcrunch_articles.json'},
    dag=dag,
)

#NOTE:Imported the scrape_techcrunch function from main.py
#NOTE Set up a basic DAG with default arguments
#NOTE Created a PythonOperator task that calls the scrape_techcrunch function
#NOTE Added the ability to specify the output file path