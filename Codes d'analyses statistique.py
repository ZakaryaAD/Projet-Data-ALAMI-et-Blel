#Transformation de runtime 

import pandas as pd

# Charger la base de données
df = pd.read_csv('movies_dataset.csv')
print(df)

# Fonction pour convertir la durée au format '1h24m' ou '39m' en minutes
def convert_to_minutes(duration):

    if 'h' in duration and 'm' in duration:
        parts = duration.split('h')
        hours = int(parts[0]) if parts[0].strip() else 0
        minutes = int(parts[1].split('m')[0].strip()) if len(parts) > 1 else 0
    elif 'm' in duration:
        hours = 0  # Si seulement 'm' est présent, considérez que les heures sont 0
        minutes = int(duration.rstrip('m'))
    else:
        return None  # Ne devrait pas arriver, mais ajoutons une vérification

    return hours * 60 + minutes
   
    

def convert_to_dd_mm_yyyy_theater(date_str):
    """J'ai du separer en deux fonction car la colonne release date theater est trop differente de streaming, il y a des terme en plus en trop de valeurs manquante"""
        # Vérifier si la valeur est NaN, il y a pas mal de valeurs problématique dans release date theater
    if pd.isna(date_str):
        return None
        # Diviser la chaîne en mots
    date_parts = date_str.split()

        # Extraire la date sans les informations supplémentaires (Wide, Limited, etc.) C'est mots se trouvent génétalement dans Release date theater 
    date_str = ' '.join(date_parts[:-1])

        # Convertir la date en format datetime
    date_obj = pd.to_datetime(date_str, format='%b %d, %Y', errors='coerce', dayfirst=True)
    formatted_date = date_obj.strftime('%d/%m/%Y')
    return formatted_date

    
    
def convert_to_dd_mm_yyyy_streaming(date_str):
   
        # Vérifier si la valeur est NaN
    if pd.isna(date_str):
        return None

    # Convertir la date en format datetime
    date_obj = pd.to_datetime(date_str, format='%b %d, %Y')
    # Formater la date en "JJ/MM/AAAA"
    formatted_date = date_obj.strftime('%d/%m/%Y')
    return formatted_date

# Fonction pour compter le nombre de valeurs manquantes par colonne
def count_missing_values(df):
    missing_values_count = df.isnull().sum()
    total_values = len(df)
    missing_values_percentage = (missing_values_count / total_values) * 100
    missing_values_info = pd.DataFrame({
        'Nombre de valeurs manquantes': missing_values_count,
        'Pourcentage de valeurs manquantes': missing_values_percentage
    })
    return missing_values_info
  
# Afficher le compte des valeurs manquantes pour chaque colonne
print(count_missing_values(df))


# Utiliser la casse exacte des noms de colonnes de votre DataFrame
df['Release Date (Theaters)'] = df['Release Date (Theaters)'].apply(convert_to_dd_mm_yyyy_theater)
df['Release Date (Streaming)'] = df['Release Date (Streaming)'].apply(convert_to_dd_mm_yyyy_streaming)

# Appliquer la fonction de conversion à la colonne 'runtime'
df['Runtime'] = df['Runtime'].apply(convert_to_minutes)

# Afficher le DataFrame avec les durées et dates  converties
print(df['Runtime'])

# Afficher le DataFrame avec les dates converties
print(df[['Release Date (Theaters)', 'Release Date (Streaming)']])

### ICI COMMENCE LE CODE DE SCRAAPING DU top 100 des meilleurs acteurs 

import requests
from bs4 import BeautifulSoup

def scrape_topito_top_actors(url, number_of_actors):
    response = requests.get(url)
    actors_list = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        actors_elements = soup.find_all('h2', class_='item-title')  # Mise à jour du sélecteur

        # Ajouter les noms des acteurs à la liste
        for i, actor_element in enumerate(actors_elements[:number_of_actors+1]):
            actor_name = actor_element.get_text(strip=True)
            actors_list.append(actor_name)

    else:
        print(f"Échec de la récupération de la page. Status code: {response.status_code}")

    return list(set(actors_list))




# URL de la page Topito
url_topito_top_actors = 'https://www.topito.com/top-meilleurs-acteurs-americains'

# Spécifier le nombre d'acteurs que vous voulez obtenir (Top 100 dans ce cas)
number_of_actors = 100

# Obtenir et afficher la liste des meilleurs acteurs via le scraping
acteurs = scrape_topito_top_actors(url_topito_top_actors, number_of_actors)
print(acteurs, len(acteurs))


