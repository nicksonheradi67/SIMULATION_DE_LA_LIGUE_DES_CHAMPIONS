import sys
from team_manager import charger_equipes
from match_simulator import tirage_groupes, jouer_phase_groupes, classement_groupes, simuler_match
from tournament_logic import construire_confrontations
from stats_generator import afficher_stats, sauvegarder_stats

def lancer_simulation():
    print("\n🔵 Bienvenue dans la SIMULATION DE LA LIGUE DES CHAMPIONS 🔵\n")

    # 1. Charger les équipes
    equipes = charger_equipes()

    # 2. Tirage au sort des groupes
    groupes = tirage_groupes(equipes)

    # 3. Phase de groupes (3 journées)
    groupes = jouer_phase_groupes(groupes)

    # 4. Classement des groupes et qualifiés
    qualifiés, _ = classement_groupes(groupes, simuler_match)

    # 5. Collecte des stats complètes
    toutes_equipes = [e for equipes_groupe in groupes.values() for e in equipes_groupe]

    # 6. Phases à élimination directe (Huitièmes → Finale)
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
                gagnants.append(e1)
            elif score2 > score1:
                gagnants.append(e2)
            else:
                from random import choice
                gagnant = choice([e1, e2])
                print(f"⚽ Tirs au but : {gagnant['nom']} se qualifie")
                gagnants.append(gagnant)

        if len(gagnants) == 1:
            vainqueur = gagnants[0]
            break

        en_cours = construire_confrontations(gagnants)
        phase_num += 1

    # 7. Affichage des stats finales
    afficher_stats(toutes_equipes, qualifiés, vainqueur)

    # 8. Sauvegarde JSON
    sauvegarder_stats(toutes_equipes, qualifiés, vainqueur)


# ✅ Lancement automatique si exécuté directement
if __name__ == "__main__":
    try:
        lancer_simulation()
    except Exception as e:
        print(f"\n❌ Une erreur est survenue : {e}")
        sys.exit(1)
