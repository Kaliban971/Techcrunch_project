FROM apache/airflow:2.7.1

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Installer directement les dépendances nécessaires
RUN pip install --no-cache-dir parsel requests icecream lxml lxml-html-clean
