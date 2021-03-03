# coding: utf-8

import datetime as dt
from uuid import uuid4

from .players import Player

class Round:
    """Contient les informations Date de debut et de fin,
     et listes des matchs à venir"""
    N_ROUND = 0

    def __init__(self, players: list):
        self.id = str(uuid4())
        self.name = 'Round {}'.format(Round.N_ROUND)
        self.start = ''
        self.end = ''
        self.matchs = []
        self.players = players

    def __repr__(self):
        return self.name

    def new_round(self):
        Round.N_ROUND += 1
        self.name = 'Round {}'.format(Round.N_ROUND)
        self.start = dt.datetime.now()
        self.define_matchs_in_round()

    def add_match(self, match):
        """

        :param tuple match: tuple provenant d'un objet Match
        """
        self.matchs.append(match)

    def end_round(self):
        """

        Method called at end of rounds
        """
        self.end = dt.datetime.now()

    def sort_player(self, players: list[Player], reversed=True) -> list:
        if reversed:
            players.sort(reverse=True, key=lambda x: (int(x.point), int(x.elo)))
        else:
            players.sort(reverse=False, key=lambda x: (int(x.point), int(x.elo)))
        return players

    def already_played(self, players) -> bool:
        """
        Permet de retourner un bool sur le fait d'avoir deja jouer contre l'adversaire.
        """
        #if
        return

    def define_matchs_in_round(self) -> list:
        nb_joueur = len(self.players)
        if self.N_ROUND == 1:
            """ Definition du premier tour"""

            self.players = self.sort_player(self.players)
            nb_joueur = len(self.players)
            if Player.isactiveplayerlistpair():
                players_list_1 = self.players[:nb_joueur // 2]
                players_list_2 = self.players[nb_joueur // 2:]

                first_round = list(zip(players_list_1, players_list_2))
                return first_round

            else:
                print("Il manque un joueur pour générer toutes les paires")
                """a retoucher dans controler et players"""

        elif self.N_ROUND == 2:
            """ Definition des autres tours
            """
            free_players = self.sort_player(self.players, False)
            already_in_round = []
            other_round = []

            while len(free_players):
                player1 = free_players.pop()
                player2 = free_players.pop()
                already_in_round.append(player1)
                already_in_round.append(player2)
                other_round.append((player1, player2))
            return other_round

    def display_match(self):
        """
        Method display match informations
        """
        print("\n{0} Début: {1} Fin: {2}".format(self.name, self.start,
                                                 self.end, ))
        for nb in range(len(self.matchs)):
            print("{0} {1} VS {2} {3}".format(self.matchs[nb][0][0],
                                              self.matchs[nb][0][1],
                                              self.matchs[nb][1][1],
                                              self.matchs[nb][1][0]))

if __name__ == '__main__':

    round = Round()
    round = round.define_matchs_in_round()
    print(round)