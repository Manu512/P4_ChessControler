# coding: utf-8
from tinydb import TinyDB
from datetime import datetime as dt


class Player:
    """
    Classe qui va gérer l'ensemble des joueurs. Participant ou non au tournoi.
    """
    NB_PLAYER = 0
    PLAYERS = []

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.first_name = kwargs['first_name']
        self.dob = kwargs['dob']
        self._genre = kwargs['_genre']
        self.elo = 0
        self.point = 0
        self.versus = []
        self.status = False
        Player.NB_PLAYER = Player.NB_PLAYER + 1
        self._id = Player.NB_PLAYER

        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)
        Player.PLAYERS.append(self)

    def __repr__(self):
        return "{} {} - elo : {} - Pts : {} - Engagé : {}".format(self.name,
                                                                  self.first_name,
                                                                  self.elo,
                                                                  self.point,
                                                                  self.status)

    @property
    def age(self) -> int:
        """
        Propriété permettant de calculer l'age a l'aide de la date
        d'anniversaire.
        """
        birth = dt.strptime(self.dob, '%d/%m/%Y')
        today = dt.today()
        return today.year - birth.year - (
                    (today.month, today.day) < (birth.month, birth.day))

    @property
    def sexe(self) -> str:
        if self._genre == 'F':
            sexe = 'Femme'
        else:
            sexe = 'Homme'
        return sexe

    def update_classement(self, new_classement: int):
        self.elo = new_classement

    def update_dob(self, new_dob: str):
        self.dob = new_dob

    def win_round(self):
        self.point += 1

    def equality_round(self):
        self.point += 0.5

    def add_versus(self, tour):
        self.versus.append(tour)

    @classmethod
    def save_players(cls):
        """
        Methode de classe permettant de sauvegarder l'ensemble des joueurs.


        Class method allowing all players to be saved.
        """
        db = TinyDB('players.json')
        players_db = db.table('players')
        players_db.truncate()
        serialized_players = [cls.player.__serialize_player() for cls.player
                              in cls.PLAYERS]
        players_db.insert_multiple(serialized_players)

    def __serialize_player(self):
        self.data = {"_id": self._id,
                     "name": self.name,
                     "first_name": self.first_name,
                     "dob": self.dob,
                     "_genre": self._genre,
                     "elo": self.elo,
                     "score": self.point,
                     "versus": self.versus,
                     "status": self.status}
        return self.data

    @classmethod
    def load_players(cls):
        """
        Methode de classe permettant de charger l'ensemble des joueurs connus.


        Class method allowing all players to be loaded.
        """
        players_db = cls.player_db_acces()
        serialized_players_list = players_db.all()
        [Player(**data) for data in serialized_players_list]

    @classmethod
    def list_all_player(cls):
        cls.players_db = cls.player_db_acces()
        cls.list_all = cls.players_db.all()
        [print(data) for data in cls.list_all]

    @staticmethod
    def player_db_acces():
        db = TinyDB('players.json')
        return db.table('players')


if __name__ == '__main__':
    Player.load_players()
    Player.list_all_player()
    print("heu....")
