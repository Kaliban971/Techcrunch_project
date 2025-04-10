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
url_accueil = "https://techcrunch.com/latest/" # Remplacez par l'URL de la page d'accueil de TechCrunch
response_accueil = requests.get(url_accueil, headers=headers) # Ajouter les headers

# Vérifier si la requête a réussi
if response_accueil.status_code == 200:
    ic("Requête réussie")
else:
    ic("Erreur lors de la requête")

selector_accueil = Selector(text=response_accueil.text) # Utiliser Selector pour analyser le HTML


# Extraire chaque carte d'article
articles = []
for card in selector_accueil.css('div.loop-card'): # boucle pour chaque carte d'article
    categorie = card.css('.loop-card__cat::text').get() or card.css('span.loop-card__cat::text').get()
    categorie_url = card.css('a.loop-card__title-link::attr(href)').get()
    lien = card.css('a.loop-card__title-link::attr(href)').get()
    titre = card.css('a.loop-card__title-link::text').get()
    auteur = card.css('a.loop-card__author::text').get() or card.css('a.loop-card__author:text').get()
    date_relative = card.css('time.loop-card__time::text').get()
    if date_relative:
        date_relative = date_relative.replace('\n\t', '') #supprimer les sauts de ligne et les espaces en début et fin de chaine de caractère
    date_absolue = card.css('time.loop-card__time::attr(datetime)').get()

#Ajouter un délai de 2 secondes entre chaque requête pour éviter de surcharger le serveur
    time.sleep(2)


#Extraire le texte des articles
    response_article = requests.get(lien, headers=headers)
    selector_article = Selector(response_article.text)

    full_article = selector_article.css('p.wp-block-paragraph::text').getall() #texte complet de l'article



    # Ajouter les informations de l'article à la liste
    articles.append({
        'Categorie': categorie,
        'URL_Categorie': categorie_url,
        'URL_Article': lien,
        'Titre': titre,
        'Auteur': auteur,
        'Date_relative': date_relative,
        'Date_absolue': date_absolue,
        'Full_article': full_article
    })




# Afficher les articles récupérés avec le texte
#for article in articles:
#afficher qu'une carte d'article
ic(articles[0])



#TODO:Voir comment faire pour gerer la pagination et récupérer les articles de toutes les pages


# Écrire dans un fichier JSON
with open("profil.json", "w", encoding="utf-8") as fichier: # le fichier est ouvert en mode écriture ("w")
    json.dump(articles, fichier, ensure_ascii=False, indent=4) # les données sont écrites dans le fichier en format JSON, avec une indentation de 4 espaces pour une meilleure lisibilité et ensure_ascii=False pour garantir que les caractères non-ASCII sont encodés correctement.