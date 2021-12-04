"""Jeu Squadro

Ce programme permet de joueur au jeu Squadro.
"""
from api import jouer_un_coup, récupérer_une_partie, lister_les_parties, créer_une_partie
from squadro import Squadro, analyser_la_ligne_de_commande
from squadro import Squadro, SquadroException
from copy import deepcopy
from time import sleep


def jouer():
    j1 = input("Nom du joueur 1: ")
    j2 = input("Nom du joueur 2: ")
    if j1 == j2:
        j2 = str(id(j2))
    partie = Squadro(j1, j2)
    while not partie.jeu_terminé():
        print(partie)
        partie.déplacer_jeton(j1, partie.demander_coup(j1))
        partie.déplacer_jeton(j2, partie.jouer_un_coup(j2)[1])
    print(f'Le gagnant est {partie.jeu_terminé()}')


def servertest(printing, t=0.1, bot=None):
    errors = []
    id_partie, prochain_joueur, état = créer_une_partie(["nagir121"], bot=bot)
    while True:
        try:
            coup_joué = Squadro(*état).jouer_un_coup(prochain_joueur)[1]
            id_partie, prochain_joueur, état = jouer_un_coup(
                id_partie, prochain_joueur, coup_joué)
            # vieil_état = deepcopy(état)
            # finding out what the enemy played
            # for i in range(5):
            #     if vieil_état[1]["pions"][i] != état[1]["pions"][i]:
            #         move = i
            # tableau_local = Squadro(*état)
            # tableau_local.déplacer_jeton(état[1]["nom"], move+1)
            # if tableau_local.état != état:
            #     errors.append((move, vieil_état))
            # vieil_état = deepcopy(état)
            if printing:
                print(Squadro(*état))
            sleep(t)
        except StopIteration as message:
            print(Squadro(*état))
            return état[1]["nom"], message, errors


def batchtest(n, printing=False, t=0, bot=None):
    result, errors = {}, []
    for _ in range(n):
        nom, message, error = servertest(printing, t, bot)
        liste_résultat = result.get(
            nom, [0, 0])
        result[nom] = [liste_résultat[0] + (1 if message == "nagir121" else 0),
                       liste_résultat[1] + (0 if message == "nagir121" else 1)]
        errors += error
    return result, errors


# python3 main.py --help (pour tester)
helpp = analyser_la_ligne_de_commande()


if __name__ == "__main__":
    # jouer()
    data = "bogos binted"
    try:
        data = (batchtest(10, printing=False, t=0, bot=3))
    except SquadroException as err:
        with open("testfile.txt", "w", encoding="utf-8") as file:
            file.write(data)
            file.write("\n" + err)
    print(data)
