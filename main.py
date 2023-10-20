import scrapper
import csv_manager
import queries
import module

#Fonction pour scrapper les données
datas = scrapper.scrapping_series()

file_path = "data/files/episodes.csv"

#Fonction pour enregistrer les données scrapper dans le fichier csv
# csv_manager.save_data_file(datas)

#Fonction pour lire les données du csv
# csv_data = csv_manager.read_episodes_csv(file_path)
# print(csv_data)

# Insertion des données du csv sur sqlite
# queries.insert_data_sqlite(csv_data)

#Insertion des données du csv sur Postgres
# queries.insert_data_postgres(file_path)

#On recupere le nombre d'épisode par pays
# country = queries.select_episodes_sorted("country")
# print(country)

#On recupere le nombre d'épisode par chaine
# channel = queries.select_episodes_sorted("channel")
# print(channel)

#On récupère la liste des noms de series sans doublon
data = queries.select_distinct_name()
#On utilise l'algorythme pour chercher le plus d'occurence d'un mot
count_word = module.count_words(data)
print(count_word)









    


