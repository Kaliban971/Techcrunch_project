from parsel import Selector
import requests
from icecream import ic
import json
import time

# Ajouter un User-Agent pour éviter d'être bloqué
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}




# Pour trouver les cartes d'articles sur la page d'accueil
url_accueil = "https://techcrunch.com/latest" # Remplacez par l'URL de la page d'accueil de TechCrunch
response_accueil = requests.get(url_accueil, headers=headers) # Ajouter les headers
selector_accueil = Selector(text=response_accueil.text) # Utiliser Selector pour analyser le HTML


# Extraire chaque carte d'article
articles = []
for card in selector_accueil.css('div.loop-card'): # boucle pour chaque carte d'article
    categorie = card.css('a.loop-card__cat::text').get() or card.css('span.loop-card__cat::text').get()
    categorie_url = card.css('a.loop-card__cat::attr(href)').get()
    titre = card.css('a.loop-card__title-link::text').get()
    lien = card.css('a.loop-card__title-link::attr(href)').get()
    auteur = card.css('a.loop-card__author::text').get() or card.css('a.loop-card__author:text').get()
    date_relative = card.css('time.loop-card__time::text').get()
    date_absolue = card.css('time.loop-card__time::attr(datetime)').get()


    time.sleep(2)


#Extraire le texte des articles
    response_article = requests.get(lien, headers=headers)
    selector_article = Selector(response_article.text)

    summary_article = selector_article.css('p#speakable-summary.wp-block-paragraph::text').getall()
    #text_article = selector_article.css('p.wp-block-paragraph').getall()





    articles.append({
        'Categorie': categorie,
        'URL_Categorie': categorie_url,
        'Titre': titre,
        'URL_Article': lien,
        'Auteur': auteur,
        'Date_relative': date_relative,
        'Date_absolue': date_absolue,
        'Summary_article': summary_article
        #'Text_article': text_article
    })




# Afficher les articles récupérés avec le texte
#for article in articles:
#afficher qu'une carte d'article
ic(articles[0])






# Écrire dans un fichier JSON
with open("profil.json", "w", encoding="utf-8") as fichier: # le fichier est ouvert en mode écriture ("w")
    json.dump(articles, fichier, indent=4) # les données sont écrites dans le fichier en format JSON, avec une indentation de 4 espaces pour une meilleure lisibilité.