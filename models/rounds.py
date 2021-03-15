# coding: utf-8

from datetime import datetime as dt
from uuid import uuid4


from tinydb import Query, TinyDB

from models.matchs import Match
from models.players import Player


class Round:

    __db = TinyDB('tournament.json')
    table_round = __db.table('round')
    """Contient les informations Date de debut et de fin,
     et listes des matches à venir"""

    def __init__(self, round_number: int, players: list, start_date=None,
                 end_date=None, matches: list = None, id: str = None):

        if isinstance(id, str) and id is not None:
            self.id = id
        else:
            self.id = str(uuid4())

        self.number = round_number
        self.name = 'Round {}'.format(self.number)

        if isinstance(start_date, str) and start_date is not None:
            self.start = start_date
        else:
            self.start = dt.now().strftime("%Y-%m-%d %H:%M")

        if isinstance(end_date, str) and end_date is not None:
            self.end = dt.fromisoformat(end_date)
        else:
            self.end = end_date

        self.players = players

        self.matches = []

        if isinstance(matches, list) and matches is not None:
            for data_match in matches:
                play = []
                for player in data_match[0]:
                    play.append([p for p in Player._PLAYERS if player == p.uuid])

                play[0] = play[0][0]
                play[1] = play[1][0]
                self.matches.append(Match(play, data_match[1]))
        else:
            self.matches = self.__define_matchs_in_round()

    def __repr__(self):
        return self.name

    def end_round(self):
        """
        Method called at end of rounds
        """
        self.end = dt.now().strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def sort_player(players: list[Player], reverse=True) -> list:
        if reverse:
            players.sort(reverse=True, key=lambda x: (int(x.point), int(x.elo)))
        else:
            players.sort(reverse=False, key=lambda x: (int(x.point), int(x.elo)))
        return players

    def __define_matchs_in_round(self) -> list:

        global second_round, first_round, other_round

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

            else:
                print("Il manque un joueur pour générer toutes les paires")
                """a retoucher dans controller et players"""

        elif self.number == 2:
            """ Definition du seconds tours
            """
            free_players = self.sort_player(self.players, False)
            second_round = []

            while len(free_players):
                player1 = free_players.pop()
                player2 = free_players.pop()
                second_round.append(Match([player1, player2]))

        else:
            """ Definition des autres tours
            """
            free_players = self.sort_player(self.players, False)
            other_round = []

            while len(free_players):
                player1 = free_players.pop()

                available_opponent = free_players.copy()

                player_to_remove = []
                for opponent_player in available_opponent:
                    if opponent_player.uuid in player1.has_met:
                        player_to_remove.append(opponent_player)

                for each_player in player_to_remove:
                    available_opponent.remove(each_player)

                player2 = available_opponent.pop()

                other_round.append(Match([player1, player2]))

        if isinstance(first_round, list):
            data = first_round
        elif isinstance(second_round, list):
            data = second_round
        else:
            data = other_round

        return data
