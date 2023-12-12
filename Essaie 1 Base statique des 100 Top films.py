import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_rotten_tomatoes(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1', class_='title', attrs={'slot': 'title', 'data-qa': 'score-panel-title'}).text.strip()
        
        # Extraction du Tomatometer
        tomatometer_wrap = soup.find('score-board-deprecated', attrs={'data-qa': 'score-panel'})
        tomatometer = tomatometer_wrap['tomatometerscore'] if tomatometer_wrap else 'N/A'

        # Extraction du Audience Score
        audience_score = tomatometer_wrap['audiencescore'] if tomatometer_wrap else 'N/A'

        # Extraction du Genre
    
        genre_label = soup.find('span', class_='genre', attrs={'data-qa': 'movie-info-item-value'})
        genre = genre_label.text.strip().replace('\n', '').replace('  ', '') if genre_label else 'N/A' # ajout de replace pour supprimer les espaces quand ya beaucoup de mots dans le genre 


        #Extraction de la date de sortie du film 

        release_date_label = soup.find('b', class_='info-item-label', string='Release Date (Theaters):')
        release_date = release_date_label.find_next('time')['datetime'] if release_date_label else 'N/A'

        #Extraction du directeur : 
        director_label = soup.find('b', class_='info-item-label', string='Director:')
        directors = [director.text.strip() for director in soup.find_all('a', attrs={'data-qa': 'movie-info-director'})] if director_label else ['N/A']
        
        #Extraction de la durée 
        duration_label = soup.find('b', class_='info-item-label', string='Runtime:')
        duration_span = duration_label.find_next('span', {'data-qa': 'movie-info-item-value'}) if duration_label else None
        duration = duration_span.text.strip() if duration_span else 'N/A'


        #Extraction du cast 
        
        cast_section = soup.find('div', {'data-qa': 'cast-section'})
        cast_items = cast_section.find_all('div', {'data-qa': 'cast-crew-item'}) if cast_section else []


        cast = []

        for i, cast_item in enumerate(cast_items): #revoie la fct enumerate 
            if i >= 5:
              break
    
            actor_name = cast_item.find('p').text.strip()
            cast.append(actor_name)  

        #Extraction du box office : 

        box_office_label = soup.find('b', class_='info-item-label', string='Box Office (Gross USA):')
        box_office_span = box_office_label.find_next('span', {'data-qa': 'movie-info-item-value'}) if box_office_label else None
        box_office = box_office_span.text.strip() if box_office_span else 'N/A'




        return {
            'Title': title,
            'Tomatometer': tomatometer,
            'Audience Score': audience_score,
            'Genre': genre,
            'Release Date': release_date,
            'Director': directors,
            'Duration': duration,
            'Cast': cast,
            'Box Office': box_office
        }
    else:
        print(f"La requête a échoué avec le code d'état {response.status_code}")


def get_top_movies():
    url = "https://www.rottentomatoes.com/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_links = soup.find_all('a', attrs={'slot': 'caption'})
        
        # Ajout d'une impression pour vérifier si les liens des films sont trouvés
        print("Liens des films trouvés:")
        for link in movie_links:
            print(link['href'])

        top_movies = [link['href'] for link in movie_links[:100]]
        
        return top_movies
    else:
        print("Erreur lors de la récupération de la page.")
        return []

# Utilisation de la fonction get_top_movies pour obtenir une liste de liens vers les 100 meilleurs films
movie_links = get_top_movies()

# Liste pour stocker les informations de chaque film
all_movies_info = []

# Scraping des informations pour chaque film
for movie_link in movie_links:
    full_movie_link = f"https://www.rottentomatoes.com{movie_link}"
    movie_info = scrape_rotten_tomatoes(full_movie_link)
    if movie_info:
        all_movies_info.append(movie_info)
        print(f"Film scrappé: {movie_info['Title']}")
    time.sleep(1)  # Pause de 1 seconde pour éviter de surcharger le serveur

# Enregistrement des données dans un fichier CSV
csv_filename = 'rotten_tomatoes_data.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Title', 'Tomatometer', 'Audience Score', 'Genre', 'Release Date', 'Director', 'Duration', 'Cast', 'Box Office']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Écrire l'en-tête du fichier CSV
    writer.writeheader()

    # Écrire les données pour chaque film
    for movie_info in all_movies_info:
        writer.writerow(movie_info)

print(f"Données enregistrées dans {csv_filename}")


#Pour continuer les variable : ajouter le code de scrapp, etendre la liste de retour et changer le fieldnames 


