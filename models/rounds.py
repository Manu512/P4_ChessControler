""" Model Round """
# coding: utf-8

from datetime import datetime as dt
from uuid import uuid4

from models.matchs import Match
from models.players import Player


class Round:
    """
    Round object which contains all the information of the rounds.
    Contains information about the start and end dates,
    and list of upcoming matches

    :param round_number: Current round number (int)
    :param players: Player object list containing the players of the tournament.
    :param start_date: Date + Start time of the round.
    :param end_date: Date + End time of the round.
    :param matches: Object List Match
    :param id: unique identifier of the Round object
    """

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
        Methode appelé en fin de round pour horodater la fin du round.
        """
        self.end = dt.now().strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def sort_player(players: list[Player], reverse=True) -> list:
        """
        Static method allows to sort the players in an ascending or descending way
        in ascending or descending order by point or by elo rating
        :param players: object list player
        :param reverse: True or False sorting order
        :return: the list of player objects sorted in the desired order

        """
        if reverse:
            players.sort(reverse=True, key=lambda x: (int(x.point), int(x.elo)))
        else:
            players.sort(reverse=False, key=lambda x: (int(x.point), int(x.elo)))
        return players

    def __define_matchs_in_round(self) -> list:
        matches = []
        if self.number == 1:    # Definition of first round matches
            self.players = self.sort_player(self.players, False)
            nb_joueur = len(self.players)
            if Player.isactiveplayerlistpair():
                """
                The list of players is divided by 2 and the 2 lists are linked together
                for the 1st round matches
                """
                players_list_1 = self.players[:nb_joueur // 2]
                players_list_2 = self.players[nb_joueur // 2:]

                while len(players_list_1):

                    player1 = players_list_1.pop()
                    player2 = players_list_2.pop()
                    matches.append(Match([player1, player2]))

            else:
                print("Il manque un joueur pour générer toutes les paires")
                """
                On pourrait ajouter un joueur factice pour générer un match 'blanc'
                Ce n'est pas preciser dans l'énoncé mais cela est envisageable.
                """

        elif self.number == 2:  # Definition of the second round matches

            free_players = self.sort_player(self.players, False)

            while len(free_players):
                player1 = free_players.pop()
                player2 = free_players.pop()
                matches.append(Match([player1, player2]))

        else:   # Definition of the meetings of the following rounds

            free_players = self.sort_player(self.players, False)

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

                matches.append(Match([player1, player2]))

        return matches
