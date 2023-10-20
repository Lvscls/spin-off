def count_words(data):
    compteur_mots = {}

    for tuple in data:
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