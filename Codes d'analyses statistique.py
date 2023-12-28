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

# Spécifier le nombre d'acteurs  (Top 100 dans ce cas)
number_of_actors = 100

# Obtenir et afficher la liste des meilleurs acteurs via le scraping
acteurs = scrape_topito_top_actors(url_topito_top_actors, number_of_actors)
acteurs = [actor.strip() for actor in acteurs]
print(acteurs, len(acteurs))


df['Number_of_Common_Actors'] = 0
df['Common_Actors'] = [[]] * len(df)

# Appliquer la comparaison pour chaque film
for i, row in df.iterrows():
    film_actors = row['actors']
    common_actors = []
    for actor in acteurs:
        if actor in film_actors:
            common_actors.append(actor)
    
    # Mettre à jour les colonnes dans le DataFrame
    df.at[i, 'Number_of_Common_Actors'] = len(common_actors)
    df.at[i, 'Common_Actors'] = common_actors

# Afficher le résultat
print(df[['Title', 'Number_of_Common_Actors', 'Common_Actors']])

# Filtrer les lignes avec Number_of_Common_Actors non nuls
#filtered_df = df.loc[df['Number_of_Common_Actors'] > 0]
# Afficher le DataFrame filtré
#print(filtered_df[['Title', 'Number_of_Common_Actors', 'Common_Actors']])


# min et max 
min_common_actors = df['Number_of_Common_Actors'].min()
max_common_actors = df['Number_of_Common_Actors'].max()

print(f"Minimum Number_of_Common_Actors: {min_common_actors}")
print(f"Maximum Number_of_Common_Actors: {max_common_actors}")


### ici jvais chercher la correlation entre number of acotrs et audience score 
### d'abord je vais enelver les % puis je vais calculer le coefficient de correlation de spearman
### le choix vient de fait que j'ai une variable pseudo continue (Audience score de 0 à 1)
# et une variable discrete prenant les valeurs 0 1 2 3 ( on peut le voir grace au max et min et au print precedent)

import pandas as pd

def convert_percentage_to_number(df, column_name):

    # Remplacer '--' par NaN
    df[column_name] = df[column_name].replace('--', pd.NA)
    
    # Remplacer pd.NA par un placeholder (par exemple, -1)
    df[column_name] = df[column_name].replace(pd.NA, -1)
    
    # Convertir les valeurs de pourcentage en nombres
    df[column_name] = df[column_name].str.rstrip('%').astype('float') / 100.0
    
    # Remplacer le placeholder par NaN à nouveau si nécessaire
    df[column_name] = df[column_name].replace(-1, pd.NA)

    return df

df = convert_percentage_to_number(df, 'AUDIENCE_SCORE')
# On peut faire la meme chose pour critics ou pour la variable finale du notebook rated 

######################## IMPORTANT  pip install scipy necessaire sinon ne fonctionne pas 

# Calculer le coefficient de corrélation de rang de Spearman
correlation_spearman = df['Number_of_Common_Actors'].corr(df['AUDIENCE_SCORE'], method='spearman')

# Afficher le coefficient de corrélation de rang de Spearman
print(f"Corrélation de rang de Spearman entre le nombre d'acteurs en commun et Audience_score : {correlation_spearman}")


#La corrélation de rang de Spearman mesure la relation monotone (pas nécessairement linéaire) entre deux variables.
# comme le coeff de correlation est positif, cela veut dire qu'il y a une relation positive et monotone entre le nombre 
# d'acteurs connue et l'audience score, cependant la valeur est tres proche de 0 donc la correlation est  faible 
# ceci peut etrz justifié par le fait que le top 100 acteurs monde proposé par le site sont américain, alors que la base de deonnée 
#contient aussi des films indiens, arabes ou autres.
# une representation graphique = diagramme de dispersion : on voit bien la tendance ascendante, et une grande dispersion des piints qui montre que la correlation est faible

"""import matplotlib.pyplot as plt

plt.scatter(df['Number_of_Common_Actors'], df['AUDIENCE_SCORE'])
plt.title('Scatter Plot entre le nombre d\'acteurs en commun et Audience_score')
plt.xlabel('Nombre d\'acteurs en commun')
plt.ylabel('Audience_score')
plt.show()"""

