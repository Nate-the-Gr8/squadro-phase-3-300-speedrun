"""
Classes:
    * Squadro - Classe qui permet de jouer au jeu Squadro
Functions:
    * move - Permet de déplacer un pion du joueur et de calculer
        l'effet sur les pions de l'autre joueur
    * get_attacked - Permet de calculer les risques qu'un pion a de se faire attaquer
    * advance_all - Permet de calculer les positions résultantes
    des pions du joueur et des pions de l'enemi en les avançant tous
"""
from datetime import datetime
import json
from os import path
from squadro_interface import SquadroInterface


class Squadro(SquadroInterface):
    """
    pass
    """

    def vérification(self, joueur_1, joueur_2):
        joueurs = [joueur_1, joueur_2]
        self.moves = [3, 1, 2, 1, 3]
        self.vertmoves = [1, 3, 2, 3, 1]
        self.allmoves = [self.moves, self.vertmoves]
        # en ordre: sabotage, danger, blocus, risque, investissement
        self.weights = [3, 1.5, 1/3, 1.5, 0.5]

        for joueur in joueurs:
            if not isinstance(joueur, dict):
                if isinstance(joueur, str):
                    joueurs[joueurs.index(joueur)] = {
                        "nom": joueur, "pions": [0 for _ in range(5)]}
                    continue
                raise SquadroException(
                    "Le joueur doit être une chaîne de caractère ou un dictionnaire.")
            if not isinstance(joueur.get("nom"), str):
                raise SquadroException(
                    "Le nom du joueur doit être une chaîne de caractère.")
            if not isinstance(joueur.get("pions"), list):
                raise SquadroException("L'objet `pions` doit être une liste.")
            if len(joueur["pions"]) != 5:
                raise SquadroException(
                    "L'objet `pions` doit posséder 5 éléments uniquement.")
            if any(not isinstance(pion, int) for pion in joueur["pions"]):
                raise SquadroException(
                    "La position des jeton doit être un entier.")
            if any(pion < 0 or pion > 12 for pion in joueur["pions"]):
                raise SquadroException(
                    "La position des jeton doit être entre 0 et 12 inclusivement.")
        # retourne seulement si les exceptions n'ont pas été soulevées
        return joueurs

    def __str__(self):
        """Afficher le plateau
        Ne faites preuve d'aucune originalité dans votre «art ascii»,
        car votre fonction sera testée par un programme et celui-ci est
        de nature intolérante (votre affichage doit être identique à
        celui illustré). Notez aussi que votre fonction sera testée
        avec plusieurs états de jeu différents.
        Args:
            état (dict): Dictionnaire représentant l'état du jeu.
            """
        table = """       . | . : | : : | : : | : . | .
         |   . | .   |   . | .   |
  ...    |     |     |     |     |      .
1 ───────┼─────┼─────┼─────┼─────┼───────
  ...    |     |     |     |     |      .
  .      |     |     |     |     |    ...
2 ───────┼─────┼─────┼─────┼─────┼───────
  .      |     |     |     |     |    ...
  ..     |     |     |     |     |     ..
3 ───────┼─────┼─────┼─────┼─────┼───────
  ..     |     |     |     |     |     ..
  .      |     |     |     |     |    ...
4 ───────┼─────┼─────┼─────┼─────┼───────
  .      |     |     |     |     |    ...
  ...    |     |     |     |     |      .
5 ───────┼─────┼─────┼─────┼─────┼───────
  ...    |     |     |     |     |      .
       . | .   |     |     |   . | .
       : | : . | . : | : . | . : | :""".splitlines()
        pion = "□□ ○"
        print("Légende:\n  □ = " + self.état[0]["nom"] +
              "\n  ■ = " + self.état[1]["nom"] + "\n")
        # pions horizontaux
        positions_x = [4, 8, 14, 20, 26, 32, 35, 31, 25, 19, 13, 7, 4]
        for i, position in enumerate(self.état[0]["pions"]):
            table[3+3*i] = table[3+3*i][:positions_x[position]] + \
                (pion if position < 6 else pion[::-1]) + \
                table[3+3*i][positions_x[position]+4:]
        positions_y = [1, 3, 6, 9, 12, 15, 16, 14, 11, 8, 5, 2, 1]
        # pions verticaux
        for i, position in enumerate(self.état[1]["pions"]):
            table[positions_y[position]] = table[positions_y[position]][:9+i*6] + \
                ("█" if position < 6 else "●") + \
                table[positions_y[position]][10+i*6:]
            table[positions_y[position]+1] = table[positions_y[position]+1][:9+i*6] + \
                ("●" if position < 6 else "█") + \
                table[positions_y[position]+1][10+i*6:]
        return "\n".join(table)

    def déplacer_jeton(self, joueur, jeton):
        nom_joueurs = [self.état[0]["nom"], self.état[1]["nom"]]
        if joueur not in nom_joueurs:
            raise SquadroException(
                "Le nom du joueur est inexistant pour le jeu en cours.")
        index_joueur = nom_joueurs.index(joueur)
        index_enemy = 1 if index_joueur == 0 else 0
        if jeton < 1 or jeton > 5:
            raise SquadroException(
                "Le numéro du jeton devrait être entre 1 à 5 inclusivement.")

        if self.jeu_terminé() is not False:
            raise SquadroException("La jeu est déjà terminée.")

        if self.état[index_joueur]["pions"][jeton-1] == 12:
            raise SquadroException(
                "Ce jeton a déjà atteint la destination finale.")

        y_position, playerpawn = jeton - \
            1, self.état[index_joueur]["pions"][jeton-1]
        player = y_position, playerpawn
        moves = self.allmoves[index_joueur] if playerpawn < 6 else [
            4-value for value in self.allmoves[index_joueur]]
        next_position = (playerpawn + moves[y_position] if playerpawn <
                         6 else 12-(playerpawn + moves[y_position]))
        for x_position, enemypawn in enumerate(self.état[index_enemy]["pions"] if playerpawn < 6 else self.état[index_enemy]["pions"][::-1]):
            temp_x, temp_player = (x_position+1 if playerpawn < 6 else 5 -
                                   x_position), playerpawn if playerpawn < 6 else 12-playerpawn
            if (next_position >= temp_x >= temp_player or next_position <= temp_x <= temp_player
                    ) and y_position+1 == (enemypawn if enemypawn < 6 else 12 - enemypawn):
                # collision!
                self.état[index_enemy]["pions"][temp_x -
                                                1] = (0 if enemypawn < 6 else 6)
                next_position = (temp_x+1 if playerpawn < 6 else temp_x-1)
                if playerpawn < 6:
                    player = temp_x
                else:
                    player = 12-(temp_x)
        if (y_position, playerpawn) == player:
            if playerpawn < 6:
                player = playerpawn + \
                    moves[y_position] if playerpawn + \
                    moves[y_position] <= 6 else 6
            else:
                player = (playerpawn + moves[y_position] if playerpawn +
                          moves[y_position] <= 12 else 12)
        elif player not in (6, 12):
            player += 1
        self.état[index_joueur]["pions"][jeton-1] = player

    def jouer_un_coup(self, joueur):
        """
        fonction pour déterminer le meilleur coup à jouer en attribuant
        un score à chaque déplacement
        métriques:
            1-détermine les collisions possibles - score: le nombre de cases que
            la collision va faire reculer - "sabotage"
            2-détermine les pions en danger et qu'il faudrait bouger - "danger"
            3-détermine les pions qui empêchent l'autre joueur de bouger - "blocus"
            4-s'il pense déplacer un pion, évaluer le score des métriques 2 et 3
            (métriques de risque) de la position suivante - "risque" et "investissement"
        """
        if joueur not in [self.état[0]["nom"], self.état[1]["nom"]]:
            raise SquadroException(
                "Le nom du joueur est inexistant pour le jeu en cours.")
        playerindex, scores = [self.état[0]["nom"], self.état[1]["nom"]].index(joueur), [
            0, 0, 0, 0, 0]
        enemyindex = 0 if playerindex == 1 else 1
        # en ordre: sabotage, danger, blocus, risque, investissement

        # trouver combien de tours un pion a pris pour se rendre là

        def nombre_de_tours(board):
            board = Squadro(*board.état_jeu())
            for j in range(2):
                # not choosing the right allmoves
                board.état[j]["pions"] = [8 - ((12-pion)/self.choose_moves(j, i)) if pion > 6 else pion /
                                          self.choose_moves(j, i) for i, pion in enumerate(board.état[j]["pions"])]
            return board

        def evaluate_score(board1, board2):
            return sum(nombre_de_tours(board2).état[playerindex]["pions"]) - sum(nombre_de_tours(board2).état[enemyindex]["pions"]) - (sum(nombre_de_tours(board1).état[playerindex]["pions"]) - sum(nombre_de_tours(board1).état[enemyindex]["pions"]))

        board1 = Squadro(*self.état_jeu())
        for pion in range(5):
            if self.état[playerindex]["pions"][pion] != 12:
                # board1 is the baseline reference, board2 is the modified board and board3 is an alternative reference (for future projections)
                # sabotage
                board2 = Squadro(*board1.état_jeu())
                try:
                    board2.déplacer_jeton(joueur, pion+1)
                except SquadroException:
                    pass
                scores[pion] += self.weights[0] * \
                    evaluate_score(board1, board2)
                # danger
                board3 = Squadro(*board1.état_jeu())
                board3.risk(playerindex, pion)
                scores[pion] += self.weights[1] * \
                    evaluate_score(board1, board3)
                # blocus
                board2 = Squadro(*board1.état_jeu())
                board2.advance_all(self.état[enemyindex]["nom"])
                board3 = Squadro(*board2.état_jeu())
                try:
                    board2.déplacer_jeton(joueur, pion+1)
                except SquadroException:
                    pass
                scores[pion] += self.weights[2] * \
                    evaluate_score(board3, board2)
                # risque
                try:
                    board1.déplacer_jeton(joueur, pion+1)
                except SquadroException:
                    pass
                board2.risk(playerindex, pion)
                scores[pion] += self.weights[3] * \
                    evaluate_score(board1, board2)
                # investissement
                board2 = Squadro(*board1.état_jeu())
                if board2.jeu_terminé() is not False:
                    continue
                board2.advance_all(self.état[enemyindex]["nom"])
                board2.advance_all(self.état[enemyindex]["nom"])
                board3 = Squadro(*board2.état_jeu())
                if board2.état[playerindex]["pions"][pion] == 12 or board2.jeu_terminé() is not False:
                    continue
                    # j'arrive tout de même parfois à l'exception du jeu terminé malgré le if
                try:
                    board2.déplacer_jeton(joueur, pion+1)
                except SquadroException:
                    pass
                scores[pion] += self.weights[4] * \
                    evaluate_score(board3, board2)

        # blocus

        # Évaluation des résultats - optimise pour trouver le meilleur déplacement
        while True:
            allmoves = scores.index(max(scores))
            if self.état[playerindex]["pions"][allmoves] != 12:
                return (joueur, allmoves+1)
            scores[allmoves] = -2147483647

    def demander_coup(self, joueur):
        if joueur not in (self.état[0]["nom"], self.état[1]["nom"]):
            raise SquadroException(
                "Le nom du joueur est inexistant pour le jeu en cours.")
        jeton = int(input("Quel jeton voulez-vous jouer? "))
        if jeton < 1 or jeton > 5:
            raise SquadroException(
                "Le numéro du jeton devrait être entre 1 à 5 inclusivement.")
        if self.état[[self.état[0]["nom"],
                      self.état[1]["nom"]].index(joueur)]["pions"][jeton-1] == 12:
            raise SquadroException(
                "Ce jeton a déjà atteint la destination finale.")
        return jeton

    def jeu_terminé(self):
        for joueur in self.état:
            endcount = 0
            for pion in joueur["pions"]:
                if pion == 12:
                    endcount += 1
            if endcount >= 4:
                return joueur["nom"]
        return False

    def choose_moves(self, playerindex, pion):
        if self.état[playerindex]["pions"][pion] < 6:
            return self.allmoves[playerindex][pion]
        return self.allmoves[0 if playerindex == 1 else 1][pion]

    def risk(self, playerindex, pion):
        y_position, enemy = pion, self.état[0 if playerindex ==
                                            1 else 1]["pions"]
        # the score calculated from this function will likely be too high
        try:
            attackerindex = enemy.index(
                self.état[playerindex]["pions"][pion] if self.état[playerindex]["pions"][pion] < 6 else 12 - self.état[playerindex]["pions"][pion])
        except ValueError:
            # not perfect but should be close to it (sabotage metric feedbacks into this metric in that case)
            for jeton in range(5):
                if self.état[playerindex]["pions"][jeton] != 12:
                    try:
                        self.déplacer_jeton(
                            self.état[playerindex]["nom"], jeton+1)
                    except SquadroException:
                        return
            return
        if attackerindex != -1 and enemy[attackerindex] < (
            y_position if y_position <= 6 else 12-y_position) >= \
                enemy[attackerindex] + self.choose_moves(playerindex, attackerindex):
            # collision!
            self.état[playerindex]["pions"][pion] = (
                0 if self.état[playerindex]["pions"][pion] < 6 else 6)
            if self.état[playerindex]["pions"][pion] < 6:
                enemy[attackerindex] = y_position + \
                    1 if y_position+1 <= 6 else 6
            else:
                enemy[attackerindex] = y_position + \
                    7 if y_position+1 <= 12 else 12

    def advance_all(self, joueur):
        for i in range(5):
            if self.état[[self.état[0]["nom"], self.état[1]["nom"]].index(joueur)]["pions"][i] != 12 and not self.jeu_terminé():
                # problème: cette condition ne semble pas protéger de tenter de jouer avec un jeu terminé.
                self.déplacer_jeton(joueur, i+1)


def enregistrer_partie_local(identifiant, prochain_joueur, état, gagnant):
    filename, parties = f"{état[0]['nom']}-{état[1]['nom']}.json", []
    # trying to get the savefile
    if path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            parties = json.load(file)
    try:
        # verifying wether the game already exists and modifying if necessary
        indexpartie = [partie["id"]
                       for partie in parties].index(identifiant)
        parties[indexpartie]["état"], parties[indexpartie]["prochain_joueur"], parties[indexpartie]["gagnant"] = état, prochain_joueur, gagnant
    except ValueError:
        # creating a new game save if it doesn't exist
        partie = {}
        partie["id"], partie["date"], partie["prochain_joueur"], partie["joueurs"], partie["état"], partie["gagnant"] = identifiant, str(
            datetime.today().replace(microsecond=0)), prochain_joueur, [état[0]["nom"], état[1]["nom"]], état, gagnant
        parties.append(partie)

    # writing
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(parties, file)

    #


class SquadroException(Exception):
    """
    Classe d'exception du jeu squadro
    """

    def __str__(self):
        return f"SquadroException: {self.args}"


if __name__ == "__main__":
    enregistrer_partie_local("1234567", "jacob", [{"nom": "nate", "pions": [
                             7, 3, 12, 12, 12]}, {"nom": "robot", "pions": [2, 12, 12, 10, 2]}], "null")
    # squadro = Squadro({"nom": "anth", "pions": [7, 3, 12, 12, 12]}, {
    #     "nom": "robot", "pions": [2, 12, 12, 10, 2]})
    # print(squadro)
