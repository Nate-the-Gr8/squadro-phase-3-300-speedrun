"""Jeu Squadro

Ce programme permet de joueur au jeu Squadro.
"""
from squadro import Squadro
from api import jouer_un_coup, récupérer_une_partie, lister_les_parties, créer_une_partie


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


def servertest():
    j1 = "Terminator"
    créer_une_partie(["nagir121"])


if __name__ == "__main__":
    jouer()
