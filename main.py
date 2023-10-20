import requests
from bs4 import BeautifulSoup


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

# infos = scrapping_series()

def save_data_file(infos):
    csv_file = "data/files/episodes.csv"
    with open(csv_file, "w") as file:
        file.write("Name,Saison,Episode,Date,Channel,Country,Href,Date\n")
        for row in infos:
            row_data = ",".join(row)
            file.write(row_data + "\n")

    print(f"Data has been saved to {csv_file}")

# save_data_file(infos)

def read_episodes_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        headers = lines[0].strip().split(',')
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

csv_file = "data/files/episodes.csv"
episodes_data = read_episodes_csv(csv_file)
for episode in episodes_data:
    print(episode)