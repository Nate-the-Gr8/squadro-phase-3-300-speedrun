"""Jeu Squadro

Ce programme permet de joueur au jeu Squadro.
"""
from api import jouer_un_coup, récupérer_une_partie, lister_les_parties, créer_une_partie
from squadro import Squadro, analyser_la_ligne_de_commande, lister_les_parties_local
from squadro import Squadro, SquadroException
from copy import deepcopy
from time import sleep


def jouer():
    args = analyser_la_ligne_de_commande()
    iduls = args.IDUL
    if args.parties:
        if args.local:
            print(lister_les_parties_local(iduls))
        else:
            print(lister_les_parties(iduls))
    partie = Squadro()

    print(f'Le gagnant est {partie.jeu_terminé()}')


def servertest(printing=False, t=0.1, bot=None):
    errors = []
    id_partie, prochain_joueur, état = créer_une_partie(["nagir121"], bot=bot)
    while True:
        try:
            tableau_local = Squadro(*deepcopy(état))
            coup_joué = Squadro(*état).jouer_un_coup(prochain_joueur)[1]
            id_partie, prochain_joueur, état = jouer_un_coup(
                id_partie, prochain_joueur, coup_joué)
            # finding out what the enemy played
            tableau_local.déplacer_jeton("nagir121", coup_joué)
            for i in range(5):
                if tableau_local.état[1]["pions"][i] != état[1]["pions"][i]:
                    move = i
            tableau_local.déplacer_jeton(état[1]["nom"], move+1)
            if tableau_local.état != état:
                errors.append((move, tableau_local.état))
            if printing:
                print(Squadro(*état))
            sleep(t)
        except StopIteration as message:
            # print(Squadro(*état))
            print(str(message) + " won!")
            return état[1]["nom"], message, errors


def batchtest(n, printing=False, t=0, bot=None):
    result, errors = {}, []
    for _ in range(n):
        nom, message, error = servertest(printing, t, bot)
        liste_résultat = result.get(
            nom, [0, 0])
        result[nom] = [liste_résultat[0] + (1 if str(message) == "nagir121" else 0),
                       liste_résultat[1] + (0 if str(message) == "nagir121" else 1)]
        errors += error
    return result, errors


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
