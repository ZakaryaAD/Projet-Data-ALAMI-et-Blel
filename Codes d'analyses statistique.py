#Transformation de runtime 

import pandas as pd

# Charger la base de données
df = pd.read_csv('movies_dataset.csv')

# Fonction pour convertir la durée au format '1h24m' ou '39m' en minutes
def convert_to_minutes(duration):
    try:
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
    except Exception as e:
        print(f"Erreur pour la valeur {duration}: {e}")
        return None
    


# Appliquer la fonction de conversion à la colonne 'runtime'
df['Runtime'] = df['Runtime'].apply(convert_to_minutes)

# Afficher le DataFrame avec les durées converties
print(df['Runtime'])



