import json
import os
import random

# 🔥 Meilleure attaque
def meilleure_attaque(equipes):
    return max(equipes, key=lambda e: e["buts_marques"])

# 🛡 Meilleure défense
def meilleure_defense(equipes):
    return min(equipes, key=lambda e: e["buts_encaisses"])

# 🏅 Classement final trié
def classement_final(equipes):
    return sorted(equipes, key=lambda e: (
        e["points"],
        e["buts_marques"] - e["buts_encaisses"],
        e["buts_marques"]
    ), reverse=True)

# 💾 Sauvegarde des statistiques
def sauvegarder_stats(equipes, qualifiés, vainqueur, filename="resultats/stats.json"):
    stats = {
        "equipes": equipes,
        "qualifies": [e["nom"] for e in qualifiés],
        "vainqueur": vainqueur["nom"],
        "meilleure_attaque": meilleure_attaque(equipes)["nom"],
        "meilleure_defense": meilleure_defense(equipes)["nom"]
    }

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)

    print(f"\n📁 Statistiques sauvegardées dans {filename}")

# 📊 Affichage lisible des statistiques
def afficher_stats(equipes, qualifiés, vainqueur):
    print("\n📊 STATISTIQUES DE LA LIGUE DES CHAMPIONS")
    print(f"🏆 Vainqueur : {vainqueur['nom']}")
    print(f"🔥 Meilleure attaque : {meilleure_attaque(equipes)['nom']} ({meilleure_attaque(equipes)['buts_marques']} buts)")
    print(f"🛡 Meilleure défense : {meilleure_defense(equipes)['nom']} ({meilleure_defense(equipes)['buts_encaisses']} buts encaisses)")

    print("\n✅ Équipes qualifiées pour les huitièmes :")
    for i, e in enumerate(qualifiés, 1):
        print(f"{i}. {e['nom']} - {e['points']} pts")

    print("\n📋 Classement final des équipes :")
    for i, e in enumerate(classement_final(equipes), 1):
        print(f"{i}. {e['nom']} - {e['points']} pts ({e['buts_marques']} BM / {e['buts_encaisses']} BE)")


# ================================
# ✅ TEST COMPLET - À PARTIR DES HUITIÈMES
# ================================
if __name__ == "__main__":
    from team_manager import charger_equipes
    from match_simulator import simuler_match, classement_groupes, tirage_groupes, jouer_phase_groupes
    from tournament_logic import construire_confrontations

    print("\n=== TEST DU MODULE 4 : STATS_GENERATOR ===")

    # 1. Charger et tirer les groupes
    equipes_base = charger_equipes()
    groupes = tirage_groupes(equipes_base)
    groupes = jouer_phase_groupes(groupes)
    qualifiés, _ = classement_groupes(groupes, simuler_match)

    # 2. Récupérer toutes les équipes avec stats à jour
    equipes = [equipe for liste in groupes.values() for equipe in liste]

    # 3. Phases à élimination directe (Huitièmes → Finale)
    noms_phases = ["Huitièmes de finale", "Quarts de finale", "Demi-finales", "🏆 Finale"]
    en_cours = construire_confrontations(qualifiés)
    phase_num = 0

    while len(en_cours) >= 1:
        print(f"\n🔷 {noms_phases[phase_num]} 🔷")
        gagnants = []
        for e1, e2 in en_cours:
            score1, score2, _ = simuler_match(e1, e2)
            print(f"{e1['nom']} {score1} - {score2} {e2['nom']}")

            if score1 > score2:
                gagnant = e1
            elif score2 > score1:
                gagnant = e2
            else:
                gagnant = random.choice([e1, e2])
                print(f"⚽ Tirs au but entre {e1['nom']} et {e2['nom']} → {gagnant['nom']} qualifié")

            gagnants.append(gagnant)

        if len(gagnants) == 1:
            vainqueur = gagnants[0]
            break

        en_cours = construire_confrontations(gagnants)
        phase_num += 1

    # 4. Affichage et sauvegarde finale
    afficher_stats(equipes, qualifiés, vainqueur)
    sauvegarder_stats(equipes, qualifiés, vainqueur)
