# Projet-Data-ALAMI-et-Blel
Le projet de programmation python pour la data science.

L'objectif de notre projet est de prévoir le succès d'un film à partir de certaines caractéristiques de base. Pour ce faire, nous allons mettre en place deux modèles de predictions. 

Le notebook de rendu final est nommé Web Scraping with sélénium.

Celui ci est divisé en 4 partie : 

Tout d'abord le téléchargement de chronium qui nous permettra de générer notre base de donnée. 

Ensuite les codes de web Scrapping qui permettent de générer notre base de donnée ; comme ces codes mettent du temps à tourner, nous les avons fait tourner et avons mis la base de donnée avec laquelle on a travaillé dans "movies_dataset.csv" 

La 3eme partie concerne le nettoyage ainsi que la mise en forme de la base de donnée. Nous y effectuons plusieurs transformations de variables et autres manipulations qui semblent pertinente dans le cas de notre base (Conversion en pourcentage, mise en forme des date, mise en forme du runtime etc...).

Enfin, la quatrieme partie s'interesse à deux modeles : Random forest et Linear Regression.

Les autres documents présents dans le git ne sont pas à prendre en compte. 

Le document nommé "Codes d'analyse statistique" est un brouillon qui contient plusieurs version de code qui pour certaines n'ont pas été retenue dans le notebook final. C'est un moyen de mettre en commun avant de passer sur le notebook et d'eviter de push / pull en meme temps. 

Le document nommé " Essaie 1 base statique" correspond à un premier essaie de web scrapping en utilisant Beautiful soup mais sans utiliser d'API. il etait impossible de générer des films aléatoirement, seulement de prendre le TOP 100 des films. Ce code n'a pas été retenu, et l'usage de selenium a été privilégié. 











