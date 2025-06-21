import json
import random

def generer_equipes():
    noms_equipes = [
        "Manchester City", "RB Leipzig", "Crvena Zvezda", "Young Boys",
        "Barcelona", "Porto", "Shakhtar Donetsk", "Royal Antwerp",
        "Real Madrid", "Napoli", "Braga", "Union Berlin",
        "Bayern Munich", "Copenhagen", "Galatasaray", "Manchester United",
        "Arsenal", "PSV Eindhoven", "Lens", "Sevilla",
        "Atletico Madrid", "Lazio", "Feyenoord", "Celtic",
        "Inter Milan", "Benfica", "Real Sociedad", "Salzburg",
        "AC Milan", "Newcastle United", "Paris Saint-Germain", "Union Saint-Gilloise"  ]

    equipes = []
    for nom in noms_equipes:
        equipe = {
            "nom": nom,
            "force": random.randint(50, 100)
        }
        equipes.append(equipe)

    return equipes

def sauvegarder_equipes(equipes, nom_fichier="equipes.json"):
    with open(nom_fichier, "w") as f:
        json.dump(equipes, f, indent=4)
    print(f"{len(equipes)} équipes sauvegardées dans {nom_fichier}")

def charger_equipes(nom_fichier="equipes.json"):
    with open(nom_fichier, "r") as f:
        return json.load(f)


# Test
if __name__ == "__main__":
    equipes = generer_equipes()
    sauvegarder_equipes(equipes)

    # 🔍 Affichage des équipes avec leur force
    print("\n Équipes générées :\n")
    for equipe in equipes:
        print(f"{equipe['nom']} - Force : {equipe['force']}")
