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