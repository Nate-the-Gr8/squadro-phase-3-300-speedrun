"""Jeu Squadro

Ce programme permet de joueur au jeu Squadro.
"""
from api import jouer_un_coup, récupérer_une_partie, lister_les_parties, créer_une_partie
from squadro import Squadro, analyser_la_ligne_de_commande, lister_les_parties_local, formatter_les_parties, enregistrer_partie_local, charger_partie_local
from squadro import Squadro, SquadroException
from copy import deepcopy
from time import sleep


def servertest(printing=False, t=0.1, bot=None):
    errors = []
    id_partie, prochain_joueur, état = créer_une_partie(["nagir121"], bot=bot)
    while True:
        try:
            coup_joué = Squadro(*état).jouer_un_coup(prochain_joueur)[1]
            id_partie, prochain_joueur, état = jouer_un_coup(
                id_partie, prochain_joueur, coup_joué)
            if printing:
                print(Squadro(*état))
            sleep(t)
        except StopIteration as message:
            return état[1]["nom"], message


def choisir_partie(iduls, local=False):
    if local and len(iduls) == 1:
        iduls.append("robot")
    parties_en_cours = []
    if local:
        parties = lister_les_parties_local(iduls)
    else:
        parties = lister_les_parties(iduls)
    for partie in parties:
        if partie["gagnant"] is None:
            parties_en_cours.append(partie)
    print(formatter_les_parties(parties_en_cours))
    choix = input(
        "Quelle partie voulez-vous continuer? (0 pour créer une partie)")
    if choix == 0:
        if local:
            return Squadro(*([iduls[0], "robot"] if len(iduls) == 1 else iduls), iduls)
        else:
            return créer_une_partie(*iduls)
    elif choix - 1 < len(parties_en_cours):
        # chargement d'une partie
        if local:
            # idea: always return a tuple formed of the usual 3 parameters and create the instance of Squadro in the game loop
            return Squadro(*(charger_partie_local(parties_en_cours[choix - 1]["id"])[2]))
        # if not local
        return récupérer_une_partie(parties_en_cours[choix - 1]["id"])


def jouer():
    args = analyser_la_ligne_de_commande()
    iduls = args.IDUL
    # lister les parties
    if args.parties:
        if args.local:
            print(formatter_les_parties(lister_les_parties_local(iduls)))
        else:
            print(formatter_les_parties(lister_les_parties(iduls)))
        return
    # mode auto
    if args.automatique:
        if args.local:
            partie = Squadro("robot-1", "robot-2")
            while not partie.jeu_terminé():
                partie.déplacer_jeton(*partie.jouer_un_coup("robot-1"))
                partie.déplacer_jeton(*partie.jouer_un_coup("robot-2"))
            else:
                print(f"Le gagnant est {partie.jeu_terminé()}!")
        else:
            servertest(printing=True)

    # Ajouter le robot si la partie est locale et qu'un seul joueur joue
    partie = choisir_partie(iduls, args.local)
    # mode en ligne

    # mode local
    if len(iduls) == 1:
        iduls.append("robot")

    while not partie.jeu_terminé():
        pass
    print(f'Le gagnant est {partie.jeu_terminé()}!')


def batchtest(n, printing=False, t=0, bot=None):
    result = {}
    for _ in range(n):
        nom, message = servertest(printing, t, bot)
        liste_résultat = result.get(
            nom, [0, 0])
        result[nom] = [liste_résultat[0] + (1 if str(message) == "nagir121" else 0),
                       liste_résultat[1] + (0 if str(message) == "nagir121" else 1)]
    return result


def overalltest(n=5, printing=False, t=0):
    data = []
    try:
        for i in range(n):
            print("now against bot " + str(i+1))
            data.append(batchtest(5, printing=False, t=0, bot=i+1))
    except SquadroException as err:
        with open("testfile.txt", "w", encoding="utf-8") as file:
            file.write(data)
            file.write("\n" + err)
    print(data)

# python3 main.py --help (pour tester)
# helpp = analyser_la_ligne_de_commande()


if __name__ == "__main__":
    # print(servertest(False))
    jouer()
    # batchtest(5, bot=5)
    # overalltest()
