import random
import json
from team_manager import charger_equipes
from match_simulator import simuler_match, tirage_groupes,jouer_phase_groupes, classement_groupes

# Tirage des huitièmes : 1ers vs 2èmes sans équipes du même groupe
def tirage_huitiemes(premiers, deuxiemes, groupes_dict):
    confrontations = []
    random.shuffle(premiers)
    for premier in premiers:
        for deuxieme in deuxiemes:
            if groupes_dict[premier["nom"]] != groupes_dict[deuxieme["nom"]]:
                confrontations.append((premier, deuxieme))
                deuxiemes.remove(deuxieme)
                break
    return confrontations

# Match à élimination directe avec tirs au but si égalité
def match_elimination(e1, e2):
    score1, score2, details = simuler_match(e1, e2)
    print(details)
    
    if score1 > score2:
        return e1
    elif score2 > score1:
        return e2
    else:
        # Tirs au but
        gagnant = random.choice([e1, e2])
        print(f"⚽ Tirs au but entre {e1['nom']} et {e2['nom']} -> {gagnant['nom']}")
        return gagnant

# Phase KO (quart, demi, finale)
def jouer_phase(phase, confrontations):
    print(f"\n📣 {phase}")
    qualifiés = []
    for e1, e2 in confrontations:
        print(f"- {e1['nom']} vs {e2['nom']}")
        gagnant = match_elimination(e1, e2)
        qualifiés.append(gagnant)
    return qualifiés

def construire_confrontations(liste_equipes):
    random.shuffle(liste_equipes)
    return [(liste_equipes[i], liste_equipes[i+1]) for i in range(0, len(liste_equipes), 2)]

# Lancement complet du tournoi
def lancer_tournoi():
    equipes = charger_equipes()
    groupes = tirage_groupes(equipes)
    groupes = jouer_phase_groupes(groupes)
    qualifies, resultats_groupes = classement_groupes(groupes, simuler_match)

    # Associer chaque équipe à son groupe
    groupes_dict = {}
    for nom_groupe, equipes in groupes.items():
        for equipe in equipes:
            groupes_dict[equipe["nom"]] = nom_groupe

    # 16es de finale
    seiziemes = jouer_phase("🔹 16èmes de finale", construire_confrontations(qualifies))

    # Séparer les 1ers et 2èmes après 16es
    premiers = seiziemes[:len(seiziemes)//2]
    deuxiemes = seiziemes[len(seiziemes)//2:]

    # Tirage des huitièmes
    huitiemes = tirage_huitiemes(premiers, deuxiemes, groupes_dict)

    # Phases à élimination directe
    quarts = jouer_phase("🏆 Quarts de finale", huitiemes)
    demies = jouer_phase("⚔ Demi-finales", list(zip(quarts[::2], quarts[1::2])))
    finale = jouer_phase("🏁 Finale", [(demies[0], demies[1])])

    # Résultat
    vainqueur = finale[0]
    print(f"\n🏅 Le vainqueur de la Ligue des Champions est : {vainqueur['nom']}")

    # Sauvegarde des qualifiés (optionnel)
    with open("qualifies.json", "w", encoding="utf-8") as f:
        json.dump(qualifies, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    lancer_tournoi()
