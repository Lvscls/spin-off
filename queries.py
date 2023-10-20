from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import sqlite3
from csv_manager import read_episodes_csv

def get_connection_sqlite():
    conn = sqlite3.connect("data/databases/database.db")
    return conn

def insert_data_sqlite(data):
    conn = get_connection_sqlite()

    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS episodes(
            id INTEGER PRIMARY KEY,
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
    
def insert_duration_sqlite(duration,id):
    conn = get_connection_sqlite()
    
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS durations(
            id INTEGER PRIMARY KEY,
            duration TEXT,
            episode INTEGER
            FOREIGN KEY(episode) REFERENCES episodes(id)
        )
        '''
    )
    conn.commit()
    cur.execute(
        "INSERT INTO durations (duration, episode) VALUES (?,?)",
        duration,id
    )
    conn.commit()
    conn.close()

"""Requetes utiles"""
def select_episodes_sorted(data):
    conn = get_connection_sqlite()
    cur = conn.cursor()
    cur.execute(f"SELECT {data}, COUNT(name) AS Nombre_episodes FROM episodes GROUP BY {data}")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def select_distinct_name():
    conn = get_connection_sqlite()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT name FROM episodes")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
    


def select_href():
    conn = get_connection_sqlite()
    cur = conn.cursor()
    cur.execute("SELECT href FROM episodes WHERE channel = 'Apple TV+' ")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def select_consecutive():
    conn = get_connection_sqlite()
    cur = conn.cursor()
    cur.execute('''
        SELECT DISTINCT date
        FROM episodes
    ''')
    dates_octobre = [date[0] for date in cur.fetchall()]

    # Créer une liste pour stocker les chaînes actives chaque jour
    chaines_actives = []

    # Créer une liste pour stocker le nombre de jours consécutifs actuels
    jours_consecutifs_actuels = []
    max_jours_consecutifs = 0
    chaines_max_consecutifs = []
    nombre_jours_consecutifs = 0

    for date in dates_octobre:
        # Exécuter une requête SQL pour obtenir les chaînes actives ce jour-là
        cur.execute('''
            SELECT DISTINCT channel
            FROM episodes
            WHERE date = ?
        ''', (date,))

        chaines_jour = [chaine[0] for chaine in cur.fetchall()]

        # Vérifier si les chaînes actives ce jour sont les mêmes qu'hier
        if chaines_jour == chaines_actives:
            jours_consecutifs_actuels.append(date)
            nombre_jours_consecutifs += 1
            max_jours_consecutifs = nombre_jours_consecutifs
        else:
            # Nouvelle journée avec des chaînes différentes
            if nombre_jours_consecutifs > max_jours_consecutifs:
                max_jours_consecutifs = nombre_jours_consecutifs
                chaines_max_consecutifs = chaines_actives
            nombre_jours_consecutifs = 1
            jours_consecutifs_actuels = [date]

        chaines_actives = chaines_jour

    return chaines_max_consecutifs, max_jours_consecutifs
    

"""Insertion data postgres"""
def insert_data_postgres(csv_file):
    episodes_data = read_episodes_csv(csv_file)
    
    episodes_data = pd.read_csv(csv_file)

    URL_DB = "postgres://course_pyth_5801:Z1cufoxTonxlgtnmHFNb@course-pyth-5801.postgresql.a.osc-fr1.scalingo-dbs.com:32624/course_pyth_5801?sslmode=prefer"
    URL_DB_SQLACHEMY = f"postgresql+psycopg2{URL_DB[8:]}"

    engine = create_engine(URL_DB_SQLACHEMY, connect_args={"sslmode": "allow"})

    episodes_data.to_sql("episodes", engine, if_exists="replace", index=False)

    engine.dispose()