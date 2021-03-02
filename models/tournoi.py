# coding: utf-8

from datetime import datetime as dt
from uuid import uuid4


class Tournoi:
    NAME = "Tournoi d'échec"
    NB_ROUND = 4
    TIMER = "Bullet"
    DESCRIPTION = ""

    def __init__(self):
        """

        :param name: Nom du tournoi
        :type name: str
        :param int nb_round: Nombre de tour
        :type nb_round: int
        :param timer: Contrôle du temps (Bullet, Blitz, Coup Rapide)
        :type timer: int
        """
        self.id = str(uuid4())
        self.name = self.NAME
        self.date = dt.today()
        self.nb_round = self.NB_ROUND
        self.round = []
        self.player = []
        self.timer = self.TIMER
        self.Description = self.DESCRIPTION

    def __repr__(self):
        return self.name + " - " + self.round[-1].name

    def add_round(self):
        self.round.append(round())
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
        return self.round[-1].name




if __name__ == '__main__':

    echec = Tournoi()
    echec.add_round()

    round = {'player_a': 'WALDNER', 'player_b': 'BREDERECK', 'score_a': 1, 'score_b': 0}
    m = Match(**round)
    print(m)
    t = Tour()
    t.add_match(m)
    print(t)
