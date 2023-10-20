# spin-off

Pour installer l'environnement virtuel taper la commande suivante : ~/.pyenv/versions/3.11.2/bin/python -m venv env

Pensez a bien utiliser les pip show [package] dans le même terminal où vous executez vos scripts py. En utilisant la même session de terminal, vous garantissez que les versions de packages que vous inspectez avec pip show sont les mêmes que celles que vous exécutez dans votre script Python.

SQL[1/2]
# Insertion des épisodes en base de données sqlite 3 et postgres

Nous avons utilisé la manière classique pour insérer les épisodes en sqlite.

Par contre pour postgres nous avons utilisé la librairie pandas qui simplifie beaucoup l'insertion.

Algorithmie[1/2]
# 3 chaines qui ont le plus d'épisodes :

Requête : SELECT channel, COUNT(name) AS Nombre_episodes FROM episodes GROUP BY channel ORDER BY Nombre_episodes DESC LIMIT 3
('Netflix', 109)
('Disney+', 30)
('Prime Video', 27)

# 3 pays qui ont le plus d'épisodes

Requête SELECT country, COUNT(name) AS Nombre_episodes FROM episodes GROUP BY country DESC LIMIT 3
('Etats_Unis', 353)
('France', 76)
('Canada', 63)

# Le mot le plus utilisé

Requête SQL pour récupèrer les noms de séries sans doublons (SELECT DISTINCT name from episodes)
Ensuite on parcourt chaque tuple de la liste, on divise le titre en mots, puis on les compte à l'aide d'un dictionnaire. Enfin, on trouve le mot le plus utilisé en cherchant la clé ayant la valeur maximale dans le dictionnaire compteur_mots avec mot_plus_utilise = max(compteur_mots, key=compteur_mots.get)

# Algorythmie 2/2
On a essayé plusieurs possibilité sans trouvé de bonne façon de faire
# SQL2/2 Orchestation
On a pas a eu le temps pour gérer la récupèration d'id des episodes 