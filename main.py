"""Jeu Squadro

Ce programme permet de joueur au jeu Squadro.
"""
from time import sleep
from uuid import uuid1
from httpx import TimeoutException
from api import jouer_un_coup, récupérer_une_partie, lister_les_parties, créer_une_partie
from squadro import Squadro, SquadroException, analyser_la_ligne_de_commande,\
    lister_les_parties_local, formatter_les_parties, enregistrer_partie_local, charger_partie_local


def servertest(printing=False, delay=0.1, bot=None):
    """
    servertest: function used to test the bot implemented by the Squadro class against
    the Python classroom server in an efficient and simple way.
    Also used to run automatic games
    """
    id_partie, prochain_joueur, état = créer_une_partie(["nagir121"], bot=bot)
    while True:
        try:
            coup_joué = Squadro(*état).jouer_un_coup(prochain_joueur)[1]
            id_partie, prochain_joueur, état = jouer_un_coup(
                id_partie, prochain_joueur, coup_joué)
            if printing:
                print(Squadro(*état))
            sleep(delay)
        except StopIteration as message:
            return état[1]["nom"], message


def choisir_partie(iduls, num_players, local=False):
    """
    choisir_partie: function used to choose game in a simple and efficient manner,
    whether the game is played locally or on the Python classroom server.
    """
    if local and num_players == 1:
        iduls += ["robot"]
    parties_en_cours = []
    if local:
        parties = lister_les_parties_local(iduls)
    else:
        parties = lister_les_parties(iduls)
    for partie in parties:
        if partie["gagnant"] is None:
            parties_en_cours.append(partie)
    if len(parties) == 0:
        if local:
            return str(uuid1()), iduls[0], Squadro(*iduls).état_jeu()
        return créer_une_partie(iduls)
    print(formatter_les_parties(parties_en_cours))
    choix = input(
        "Quelle partie voulez-vous continuer? (0 pour créer une partie)")
    try:
        choix = int(choix)
    except ValueError:
        print("Caractère invalide!")
        return choisir_partie(iduls, local)
    if choix == 0:
        if local:
            return str(uuid1()), iduls[0], Squadro(*iduls).état_jeu()
        return créer_une_partie(iduls)
    if choix - 1 < len(parties_en_cours):
        # chargement d'une partie
        if local:
            return charger_partie_local(parties_en_cours[choix - 1]["id"], iduls)
        # if not local
        return récupérer_une_partie(parties_en_cours[choix - 1]["id"])
    print("Numéro de partie invalide!")
    return choisir_partie(iduls, local)


def jouer():
    """
    jouer: mainloop function
    """
    args = analyser_la_ligne_de_commande()
    iduls = args.IDUL
    num_players = len(iduls)
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
                print(partie)
                if partie.jeu_terminé() is not False:
                    break
                sleep(0.2)
                partie.déplacer_jeton(*partie.jouer_un_coup("robot-2"))
                sleep(0.2)
                print(partie)
            print(f"Le gagnant est {partie.jeu_terminé()}!")
        else:
            print(f"Le gagnant est {servertest(printing=True)[1]}!")
        return
    # Initialisation ou récupération de la partie
    id_partie, prochain_joueur, état = choisir_partie(
        iduls, num_players, args.local)
    # mode local
    if args.local:
        partie = Squadro(*état)
        loopvar = 0
        joueurs = [état[0]["nom"], état[1]["nom"]]
        while not partie.jeu_terminé():
            # do only one action per loop and save after it.
            # verify if game is finished midloop only if the bot is playing
            print(partie)
            partie.déplacer_jeton(
                prochain_joueur, partie.demander_coup(prochain_joueur))
            loopvar += 1
            prochain_joueur = joueurs[loopvar%2]
            if num_players == 1:
                enregistrer_partie_local(
                    id_partie, prochain_joueur, partie.état)
                if partie.jeu_terminé() is not False:
                    break
                partie.déplacer_jeton(*partie.jouer_un_coup(prochain_joueur))
                loopvar += 1
                prochain_joueur = joueurs[loopvar%2]
            enregistrer_partie_local(
                id_partie, prochain_joueur, partie.état)
            if partie.jeu_terminé() is not False:
                break
        print(partie)
        enregistrer_partie_local(
            id_partie, partie.état[1]["nom"], partie.état, gagnant=partie.jeu_terminé())
        print(f'Le gagnant est {partie.jeu_terminé()}!\nBien joué!')

    # mode en ligne
    while True:
        try:
            partie = Squadro(*état)
            print(partie)
            coup = partie.demander_coup(prochain_joueur)
            id_partie, prochain_joueur, état = jouer_un_coup(
                id_partie, prochain_joueur, coup)
        except StopIteration as gagnant:
            partie = Squadro(*état)
            print(f"Le gagnant est {gagnant}!\nBien joué!")
            break

    if input("Voulez-vous jouer une autre partie? (y pour rejouer)") == "y":
        jouer()


def batchtest(number, printing=False, delay=0, bot=None):
    """
    batchtest: function used to repeatedly test the bot implemented by the
    Squadro class against the Python classroom server bot.
    """
    result = {}
    for _ in range(number):
        nom, message = servertest(printing, delay, bot)
        print(f"{message} a gagné!")
        liste_résultat = result.get(
            nom, [0, 0])
        result[nom] = [liste_résultat[0] + (1 if str(message) == "nagir121" else 0),
                       liste_résultat[1] + (0 if str(message) == "nagir121" else 1)]
    return result


def overalltest(number=5, printing=False, delay=0):
    """
    overalltest: function used to repeatedly test against all the Python server bots.
    """
    data = []
    try:
        for i in range(5):
            print("now against bot " + str(i+1))
            data.append(batchtest(number, printing=printing, bot=i+1, delay=delay))
    except SquadroException as err:
        with open("overalltest logger.txt", "w", encoding="utf-8") as file:
            file.write(data)
            file.write("\n" + err)
    except TimeoutException:
        print(data)
        print("The server timed out!")
    wins = 0
    for dictionnaire in data:
        for value in dictionnaire.values():
            wins += value[0]
    print(f"Win rate: {wins/(number*5)*100}%")
    print(data)


def selftest(number):
    for _ in range(number):
        partie = Squadro("robot-1", "terminator")
        partie2 = Squadro("robot-1", "terminator")
        partie2.weights = [2.5, 1, 0.25, 1, 0.25]
        while not partie.jeu_terminé():
            partie.déplacer_jeton(*partie.jouer_un_coup("robot-1"))
            # print(partie)
            partie2.état = partie.état_jeu()
            partie.déplacer_jeton(*partie2.jouer_un_coup("terminator"))
            # print(partie)
        print(partie2.weights)
        print(f"Le gagnant est {partie.jeu_terminé()}!")



if __name__ == "__main__":
    # print(servertest(False))
    # jouer()
    # batchtest(5, bot=5)
    # overalltest(number=3)
    selftest(3)
