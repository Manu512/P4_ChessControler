# coding: utf-8

from .players import Player
from .matchs import Match
from .rounds import Round
from datetime import datetime as dt
from uuid import uuid4


class Tournoi:
    def __init__(self, name="Tournois", nb_round=4, timer=0):
        """

        :param name: Nom du tournoi
        :type name: str
        :param int nb_round: Nombre de tour
        :type nb_round: int
        :param timer: Controle du temps (Bullet, Blitz, Coup Rapide)
        :type timer: int
        """
        self.id = str(uuid4())
        self.name = name
        self.date = dt.today()
        self.nb_round = nb_round
        self.tournee = []
        self.player = []
        self.timer = timer
        self.Description = ''

    def __repr__(self):
        return self.name + " - " + self.tournee[-1].name

    def add_round(self):
        self.tournee.append(Tour())
        return

    def add_player(self, player: Player):
        self.player.append(player)
        return

    def start(self):
        """D"""
        pass

    def save(self):
        """D"""
        pass

    def load(self):
        """D Methode permettant de reprendre une partie sauvegarder"""

    @property
    def current_round(self):
        return self.tournee[-1].name




if __name__ == '__main__':

    echec = Tournoi()
    echec.add_round()

    round = {'player_a': 'WALDNER', 'player_b': 'BREDERECK', 'score_a': 1, 'score_b': 0}
    m = Match(**round)
    print(m)
    t = Tour()
    t.add_match(m)
    print(t)

    def test(essai, /, test2, test3, *, enfin, peutetre):
        print(essai)
        print(test2)
