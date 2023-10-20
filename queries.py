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
    

"""Insertion data postgres"""
def insert_data_postgres(csv_file):
    episodes_data = read_episodes_csv(csv_file)
    
    episodes_data = pd.read_csv(csv_file)

    URL_DB = "postgres://course_pyth_5801:Z1cufoxTonxlgtnmHFNb@course-pyth-5801.postgresql.a.osc-fr1.scalingo-dbs.com:32624/course_pyth_5801?sslmode=prefer"
    URL_DB_SQLACHEMY = f"postgresql+psycopg2{URL_DB[8:]}"

    engine = create_engine(URL_DB_SQLACHEMY, connect_args={"sslmode": "allow"})

    episodes_data.to_sql("episodes", engine, if_exists="replace", index=False)

    engine.dispose()