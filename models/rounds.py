# coding: utf-8

import datetime as dt
from uuid import uuid4

from models.players import Player
from models.matchs import Match


class Round:
    """Contient les informations Date de debut et de fin,
     et listes des matches à venir"""

    def __init__(self, round_number: int, players: list[Player], start_date=None,
                 end_date=None, matches: list[Match] = None):
        self.id = str(uuid4())
        self.number = round_number
        self.name = 'Round {}'.format(self.number)

        if isinstance(start_date, str) and start_date is not None:
            self.start = dt.datetime.fromisoformat(start_date)
        else:
            self.start = start_date

        if isinstance(end_date, str) and end_date is not None:
            self.end = dt.datetime.fromisoformat(end_date)
        else:
            self.end = end_date

        if isinstance(matches, str) and matches is not None:
            for data_match in matches:
                self.matches.append(*data_match)
        else:
            self.matches = []

        self.players = players

    def __repr__(self):
        return self.name

    def new_round(self):
        self.start = dt.datetime.now()
        self.matches = self.define_matchs_in_round()

    def end_round(self):
        """
        Method called at end of rounds
        """
        self.end = dt.datetime.now()

    @staticmethod
    def sort_player(players: list[Player], reversed=True) -> list:
        if reversed:
            players.sort(reverse=True, key=lambda x: (int(x.point), int(x.elo)))
        else:
            players.sort(reverse=False, key=lambda x: (int(x.point), int(x.elo)))
        return players

    def define_matchs_in_round(self) -> list:
        if self.number == 1:
            """ Definition du premier tour"""

            self.players = self.sort_player(self.players, False)
            nb_joueur = len(self.players)
            if Player.isactiveplayerlistpair():
                players_list_1 = self.players[:nb_joueur // 2]
                players_list_2 = self.players[nb_joueur // 2:]

                first_round = []

                for x in range(nb_joueur // 2):
                    player1 = players_list_1.pop()
                    player2 = players_list_2.pop()
                    first_round.append(Match([player1, player2]))
                return first_round

            else:
                print("Il manque un joueur pour générer toutes les paires")
                """a retoucher dans controler et players"""

        elif self.number == 2:
            """ Definition du seconds tours
            """
            free_players = self.sort_player(self.players, False)
            second_round = []

            while len(free_players):
                player1 = free_players.pop()
                player2 = free_players.pop()
                second_round.append(Match([player1, player2]))
            return second_round
        else:
            """ Definition des autres tours
            """
            free_players = self.sort_player(self.players, False)
            other_round = []

            while len(free_players):
                player1 = free_players.pop()

                x = -1
                while free_players[x].id in player1.has_met:
                    x -= 1
                player2 = free_players.pop(x)
                other_round.append(Match([player1, player2]))
            return other_round
