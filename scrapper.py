import requests
from bs4 import BeautifulSoup
import time

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

def scrapping_duration(result_href):
    durations = []
    for row in result_href:
        url = "https://www.spin-off.fr/" + row[0]   


        response = requests.get(url)

        text = response.text

        page = BeautifulSoup(text, "html.parser")

        div = page.find("div", class_="episode_infos_episode_format")
    
        if div:
            duration = " ".join(div.stripped_strings)
            durations.append(duration)
        
        time.sleep(1)

    return durations