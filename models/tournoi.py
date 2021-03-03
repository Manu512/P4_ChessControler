# coding: utf-8

from datetime import datetime as dt
from uuid import uuid4


class Tournoi:
    NAME = "Tournoi d'échec"
    NB_ROUND = 4
    TIMER = "Bullet"
    DESCRIPTION = ""

    def __init__(self, **kwargs):
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
        self.rounds = []
        self.players = []
        self.timer = self.TIMER
        self.Description = self.DESCRIPTION
        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)

    def __repr__(self):
        return self.name + " - " + self.rounds[-1].name

    def add_round(self):
        self.rounds.append(round())
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
        return self.rounds[-1].name

# --------------------------TinyDB parts---------------------------------------

    def save_tournament(self):
        """
        Methode de classe permettant de sauvegarder l'ensemble des joueurs.
        Class method allowing all players to be saved.
        """
        tournament_db = cls.__tournament_db_acces()
        # tournament_db.truncate()
        serialized_tournament = self.__serialize_tournament()
        tournament_db.insert(serialized_tournament)

    def __serialize_tournament(self):
        self.data = {"_id": self._id,
                     "name": self.name,
                     "first_name": self.first_name,
                     "dob": self.dob,
                     "_genre": self._genre,
                     "elo": self.elo,
                     "score": self.point,
                     "has_met": self.versus,
                     "status": self.status}
        return self.data

    @classmethod
    def load_tournament(cls):
        """
        Methode de classe permettant de charger l'ensemble des joueurs connus.


        Class method allowing all players to be loaded.
        """
        tournament_db = cls.__tournament_db_acces()
        serialized_tournament_data = tournament_db.all()
        [Tournoi(**data) for data in serialized_tournament_data]

    @staticmethod
    def __tournament_db_acces():
        db = TinyDB('tournament.json')
        return db.table('tournament')


if __name__ == '__main__':

    echec = Tournoi()
    echec.add_round()

    round = {'player_a': 'WALDNER', 'player_b': 'BREDERECK', 'score_a': 1, 'score_b': 0}
    m = Match(**round)
    print(m)
    t = Tour()
    t.add_match(m)
    print(t)
