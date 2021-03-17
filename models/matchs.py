""" Model Match """
# coding: utf-8

from models.players import Player


class Match:
    """
    Class to instantiate matches
    """
    def __init__(self, players: list, scores: list = None):
        self.players = [players[0], players[1]]
        self.score = scores

    def __repr__(self):
        """
        Returns a tuple with 2 lists: the players and the results
        """
        return str((self.players, self.score))

    def win(self, player: Player = None):
        """
        Method to fill in the score of the match and add the points.
        :param player: str
        """
        if player == self.players[0]:
            self.score = [1, 0]
        elif player == self.players[1]:
            self.score = [0, 1]
        else:
            self.score = [0.5, 0.5]
