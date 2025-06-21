import json
import random

def creer_equipes():
    """Création des équipes avec entrée utilisateur et stockage dans un fichier JSON."""
    equipes = []
    print("Veuillez entrer les noms des 32 équipes :")
    for i in range(1, 33):
        nom = input(f"Nom de l'équipe {i} : ").strip()
        force = random.randint(50, 100)
        equipe = {
            'nom': nom,
            'force': force,
            'points': 0,
            'buts_marques': 0,
            'buts_encaisses': 0
        }
        equipes.append(equipe)
    
    with open('equipes.json', 'w', encoding='utf-8') as f:
        json.dump(equipes, f, indent=4, ensure_ascii=False)

    print("Les équipes ont été enregistrées dans 'equipes.json'.")
    return equipes

def charger_equipes():
    """Charge les équipes à partir du fichier JSON."""
    try:
        with open('equipes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Le fichier 'equipes.json' est introuvable.")
        return []

def repartition_groupes(equipes):
    """Répartit les équipes dans des groupes après mélange."""
    random.shuffle(equipes)
    groupes = {}
    lettres = [chr(i) for i in range(65, 73)]  # Groupes A à H

    for i, lettre in enumerate(lettres):
        groupes[lettre] = equipes[i * 4:(i + 1) * 4]
    
    return groupes

def simuler_match(equipe1, equipe2):
    """Simule un match entre deux équipes."""
    force1, force2 = equipe1['force'], equipe2['force']
    buts1 = random.randint(0, max(1, force1 // 20))
    buts2 = random.randint(0, max(1, force2 // 20))

    equipe1['buts_marques'] += buts1
    equipe1['buts_encaisses'] += buts2
    equipe2['buts_marques'] += buts2
    equipe2['buts_encaisses'] += buts1

    if buts1 > buts2:
        equipe1['points'] += 3
    elif buts1 < buts2:
        equipe2['points'] += 3
    else:
        equipe1['points'] += 1
        equipe2['points'] += 1

    print(f"{equipe1['nom']} {buts1} - {buts2} {equipe2['nom']}")

def simuler_groupes(groupes):
    """Simule les matchs dans chaque groupe et classe les équipes."""
    for lettre, equipes in groupes.items():
        print(f"\n--- Groupe {lettre} ---")
        
        for equipe in equipes:
            equipe['points'] = 0
            equipe['buts_marques'] = 0
            equipe['buts_encaisses'] = 0
        
        for i in range(len(equipes)):
            for j in range(i + 1, len(equipes)):
                simuler_match(equipes[i], equipes[j])
        
        equipes.sort(key=lambda x: (x['points'], x['buts_marques'] - x['buts_encaisses'], x['buts_marques']), reverse=True)

        print("\nClassement :")
        for idx, equipe in enumerate(equipes, 1):
            diff = equipe['buts_marques'] - equipe['buts_encaisses']
            print(f"{idx}. {equipe['nom']} - {equipe['points']} pts (Diff: {diff})")

    return groupes

def equipes_qualifiees(groupes):
    """Retourne les équipes qualifiées pour la phase suivante."""
    qualifiees = []
    for equipes in groupes.values():
        qualifiees.extend(equipes[:2])
    
    return qualifiees

if __name__ == "__main__":
    equipes = creer_equipes()

    if equipes:
        groupes = repartition_groupes(equipes)
        groupes = simuler_groupes(groupes)
        qualifiees = equipes_qualifiees(groupes)

        with open('equipes_qualifiees.json', 'w', encoding='utf-8') as f:
            json.dump(qualifiees, f, indent=4, ensure_ascii=False)

        print("\nLes équipes qualifiées pour la phase à élimination directe ont été enregistrées dans 'equipes_qualifiees.json'.")