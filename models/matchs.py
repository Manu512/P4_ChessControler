"""Class Match"""
# coding: utf-8


class Match:
    """ Classe pour instancier les matches"""
    def __init__(self, players: list, scores: list = None):
        self.players = [players[0], players[1]]
        self.score = scores

    def __repr__(self):
        """Retour un tuple avec 2 listes celle des joueurs et celles des résultats"""
        return str((self.players, self.score))

    def win(self, player=""):
        if player == self.players[0]:
            self.score = [1, 0]
        elif player == self.players[1]:
            self.score = [0, 1]
        else:
            self.score = [0.5, 0.5]