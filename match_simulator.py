# group_stage.py
import random
from team_manager import charger_equipes

def tirage_groupes(equipes):
    random.shuffle(equipes)
    groupes = {chr(65+i): [] for i in range(8)}  # A à H

    for i, equipe in enumerate(equipes):
        groupe = chr(65 + (i % 8))
        groupes[groupe].append({
            "nom": equipe["nom"],
            "force": equipe["force"],
            "points": 0,
            "buts_marques": 0,
            "buts_encaisses": 0
        })
    
    return groupes

def simuler_match(e1, e2):
    # Score influencé par la force + aléatoire
    score1 = random.randint(0, int(e1["force"]/15 + 2))
    score2 = random.randint(0, int(e2["force"]/15 + 2))

    e1["buts_marques"] += score1
    e1["buts_encaisses"] += score2
    e2["buts_marques"] += score2
    e2["buts_encaisses"] += score1

    if score1 > score2:
        e1["points"] += 3
    elif score2 > score1:
        e2["points"] += 3
    else:
        e1["points"] += 1
        e2["points"] += 1

    details = f"{e1['nom']} {score1} - {score2} {e2['nom']}"
    return score1, score2, details

def jouer_phase_groupes(groupes):
    for groupe, equipes in groupes.items():
        print(f"\n Groupe {groupe}")
        for i in range(3):
            for j in range(i+1, 4):
                match = simuler_match(equipes[i], equipes[j])
                print(match)
    return groupes

def classement_groupes(groupes, simuler_match):
    qualifiés = []
    resultats_groupes = {}
    for nom_groupe, equipes in groupes.items():
        classement = sorted(equipes, key=lambda x: (x["points"], x["buts_marques"] - x["buts_encaisses"]), reverse=True)
        print(f"\n Classement du groupe {nom_groupe}:")
        for idx, equipe in enumerate(classement):
            print(f"{idx+1}. {equipe['nom']} - {equipe['points']} pts")
        resultats_groupes[nom_groupe] = classement
        qualifiés += classement[:2]
    return qualifiés, resultats_groupes


# Test
if __name__ == "__main__":
    equipes = charger_equipes()
    groupes = tirage_groupes(equipes)
    groupes = jouer_phase_groupes(groupes)
    qualifies = classement_groupes(groupes, simuler_match)

    print("\n✅ Équipes qualifiées pour les huitièmes de finale :")
    for idx, equipe in enumerate(qualifies, start=1):
        print(f"{idx}. {equipe}")
