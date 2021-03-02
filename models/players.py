# coding: utf-8
from tinydb import TinyDB
from datetime import datetime as dt


class Player:
    """
    Classe qui va gérer l'ensemble des joueurs. Participant ou non au tournoi.
    """
    _NB_PLAYER = 0
    _NB_ACTIVE_PLAYERS = 0
    _PLAYERS = []

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.first_name = kwargs['first_name']
        self.dob = kwargs['dob']
        self._genre = kwargs['_genre']
        self.elo = 0
        self.point = 0
        self.versus = []
        self.status = False
        Player._NB_PLAYER = Player._NB_PLAYER + 1
        self._id = Player._NB_PLAYER

        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)
        Player._PLAYERS.append(self)

    def __repr__(self):
        return "{} {} - elo : {} " \
               "- Pts : {} " \
               "- Engagé : {}".format(self.name,
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

    def switch_player_tournament(self):
        """Change le status du joueur dans le tournoi
        Change the status of the player in the tournament
        """
        if self.status:
            self.status = False
        else:
            self.status = True

    @classmethod
    def _save_players(cls):
        """
        Methode de classe permettant de sauvegarder l'ensemble des joueurs.
        Class method allowing all players to be saved.
        """
        players_db = cls.__player_db_acces()
        players_db.truncate()
        serialized_players = [cls.player.__serialize_player() for cls.player
                              in cls._PLAYERS]
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
        players_db = cls.__player_db_acces()
        serialized_players_list = players_db.all()
        [Player(**data) for data in serialized_players_list]

    @classmethod
    def _isactiveplayerlistpair(cls):
        """Method to find out if the list of active players is an even one
        Method permettant de savoir si la liste des joueurs actifs est pair
        """
        return cls._NB_ACTIVE_PLAYERS % 2

    @classmethod
    def _list_all_player(cls):
        [print(player) for player in cls._PLAYERS]

    @staticmethod
    def __player_db_acces():
        db = TinyDB('players.json')
        return db.table('players')


if __name__ == '__main__':
    Player.load_players()
    Player._list_all_player()
    print("heu....")
