# -*- coding: utf-8 -*-
"""Module d'API du jeu Squadro

Ce module permet d'interagir avec le serveur
afin de pouvoir jouer contre un adversaire robotisé.

Attributes:
    URL (str): Constante représentant le début de l'url du serveur de jeu.

Functions:
    * récupérer_parties - Récupérer la liste des parties reçus du serveur.
    * retrouver_partie - Retrouver l'état d'une partie spécifique.
    * commencer_partie - Créer une nouvelle partie et retourne l'état de cette dernière.
    * executer_coup - Exécute un coup et retourne le nouvel état de jeu.
"""
import httpx

URL = "https://pax.ulaval.ca/squadro/api2/"


def lister_les_parties(iduls):
    """Récupérer les identifiants de vos parties les plus récentes.
    Args:
        iduls (list): Liste des identifiant des joueurs.
    Returns:
        list: Liste des parties reçues du serveur,
             après avoir décodé le JSON de sa réponse.
    Raises:
        RuntimeError: Erreur levée lorsqu'il y a présence d'un message
            dans la réponse du serveur.
            """
    answer = httpx.get(URL + "parties", params={"iduls": iduls})
    if answer.status_code == 406:
        raise RuntimeError(answer.json())
    answer = answer.json()
    return answer["parties"]


def récupérer_une_partie(id_partie):
    """Retrouver une partie depuis son identifiant.
    Args:
        id_partie (str): Identifiant de la partie à récupérer.
    Returns:
        tuple: Tuple constitué de l'identifiant de la partie en cours,
            du prochain joueur à jouer et de l'état courant du jeu,
            après avoir décodé le JSON de sa réponse.
    Raises:
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        """
    answer = httpx.get(URL + "partie", params={"id": id_partie})
    if answer.status_code == 406:
        raise RuntimeError(answer.json())
    answer = answer.json()
    return (answer["id"], answer["prochain_joueur"], answer["état"])


def créer_une_partie(iduls, bot=None):
    """Débuter une nouvelle partie.
    Args:
        iduls (list): Liste de string représentant le ou les identifiant(s) du ou des joueur(s).
    Returns:
        tuple: Tuple constitué de l'identifiant de la partie en cours,
            du prochain joueur à jouer et de l'état courant du jeu,
            après avoir décodé le JSON de sa réponse.
    Raises:
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        """
    if bot is None:
        answer = httpx.post(URL + "partie", json={"iduls": iduls})
    else:
        answer = httpx.post(URL + "partie", json={"iduls": iduls, "bot": bot})
    if answer.status_code == 406:
        raise RuntimeError(answer.json())
    answer = answer.json()
    return (answer["id"], answer["prochain_joueur"], answer["état"])


def jouer_un_coup(id_partie, idul, pion):
    """Jouer votre coup dans une partie en cours
    Args:
        id_partie (str): identifiant de la partie;
        idul (str): IDUL jouant un coup;
        pion (int): Numéro du pion à déplacer.
    Returns:
        tuple: Tuple constitué de l'identifiant de la partie en cours,
            du prochain joueur à jouer et de l'état courant du jeu,
            après avoir décodé le JSON de sa réponse.
    Raises:
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        StopIteration: Erreur levée lorsqu'il y a un gagnant dans la réponse du serveur.
        """
    answer = httpx.put(
        URL + "jouer", json={"id": id_partie, "idul": idul, "pion": pion})
    if answer.status_code == 406:
        raise RuntimeError(answer.json())
    answer = answer.json()
    if answer["gagnant"] is not None:
        raise StopIteration(answer["gagnant"])
    return (answer["id"], answer["prochain_joueur"], answer["état"])
