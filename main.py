import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import sqlite3

url_spin= "https://www.spin-off.fr/calendrier_des_series.html?date=2023-10"

def scrapping_series():
    response = requests.get(url_spin)

    text = response.text

    page = BeautifulSoup(text, "html.parser")

    td = page.find_all("td", class_="td_jour")

    spans = page.find_all("span", class_="calendrier_episodes")
    
    infos = []

    for t in td:
        div_jour = t.find("div", class_="div_jour")
        if div_jour:
            date = div_jour.get("id").removeprefix("jour_")
        spans = t.find_all("span", class_="calendrier_episodes")
        for s in spans:
            name = s.find("a").text
            saison, episode = s.find_all("a")[1].text.split(".")
            channel = s.find_previous_sibling("img")['alt']
            img_channel = s.find_previous_sibling("img")
            img_country = img_channel.find_previous_sibling("img")
            country = img_country['alt']
            href = s.find("a").find_next("a")["href"]
            infos.append([name, saison, episode, channel, country, href,date])
    return infos

""" infos = scrapping_series() """

def save_data_file(infos):
    csv_file = "data/files/episodes.csv"
    with open(csv_file, "w") as file:
        file.write("Name,Saison,Episode,Channel,Country,Href,Date\n")
        for row in infos:
            row_data = ",".join(row)
            file.write(row_data + "\n")

    print(f"Insertion des données dans le {csv_file}.")

""" save_data_file(infos) """

def read_episodes_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            values = line.strip().split(',')
            name = values[0]
            saison = int(values[1])
            episode = int(values[2])
            date = values[3]
            channel = values[4]
            country = values[5]
            href = values[6]
            data.append((name, saison, episode, date, channel, country, href))
    return data

# csv_file = "data/files/episodes.csv"
# data = read_episodes_csv(csv_file)

def get_connection_sqlite():
    conn = sqlite3.connect("data/databases/database.db")
    return conn

def insert_episodes(data):
    conn = get_connection_sqlite()

    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS episodes(
            name TEXT,
            saison INTEGER,
            episode INTEGER,
            channel TEXT,
            country TEXT,
            href TEXT,
            date TEXT
        )
        '''
    )
    conn.commit()
    cur.executemany(
        "INSERT INTO episodes (name, saison, episode, channel, country, href, date) VALUES (?,?,?,?,?,?,?)",
        data,
    )
    conn.commit()

    cur.close()
    conn.close()

def select_episodes_sorted(data):
    conn = get_connection_sqlite()
    cur = conn.cursor()
    cur.execute(f"SELECT {data}, COUNT(name) AS Nombre_episodes FROM episodes GROUP BY {data}")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def select_disctinc_name():
    conn = get_connection_sqlite()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT name FROM episodes")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
    
# result = select_disctinc_name()

def count_words(data):
    compteur_mots = {}

    for tuple in result:
        titre = tuple[0] 
        mots = titre.split() 

        for mot in mots:
            mot = mot.lower()  
            if mot in compteur_mots:
                compteur_mots[mot] += 1
            else:
                compteur_mots[mot] = 1

    mot_plus_utilise = max(compteur_mots, key=compteur_mots.get)
    nb=compteur_mots[mot_plus_utilise]
    return mot_plus_utilise,nb

# most_use_word = count_words(result)

def insert_data_postgres(csv_file):
    episodes_data = read_episodes_csv(csv_file)
    
    episodes_data = pd.read_csv(csv_file)

    URL_DB = "postgres://course_pyth_5801:Z1cufoxTonxlgtnmHFNb@course-pyth-5801.postgresql.a.osc-fr1.scalingo-dbs.com:32624/course_pyth_5801?sslmode=prefer"
    URL_DB_SQLACHEMY = f"postgresql+psycopg2{URL_DB[8:]}"

    engine = create_engine(URL_DB_SQLACHEMY, connect_args={"sslmode": "allow"})

    episodes_data.to_sql("episodes", engine, if_exists="replace", index=False)

    engine.dispose()

