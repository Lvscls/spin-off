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