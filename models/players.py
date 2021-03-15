# coding: utf-8
from datetime import datetime as dt
from uuid import uuid4

from tinydb import Query, TinyDB
from tinydb.operations import delete


class Player:

    __db = TinyDB('players.json')
    __db = __db.table('players')
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
        self.has_met = []
        self.status = False
        Player._NB_PLAYER = Player._NB_PLAYER + 1
        self.id = Player._NB_PLAYER
        self.uuid = str(uuid4())

        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)
        self._PLAYERS.append(self)

    def __repr__(self):
        return "{} - {} - {} pts".format(self.id, self.fullname, self.point)

    def update_player(self):
        q = Query()
        players_table = self.__db
        player_data = self.__serialize_player()
        players_table.upsert(player_data, q.uuid == self.uuid)

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
    def fullname(self):
        return f"{self.name} {self.first_name}"

    @property
    def sexe(self) -> str:
        """
        Propriété pour afficher le genre de facon lisible
        """
        if self._genre == 'F':
            sexe = 'Femme'
        else:
            sexe = 'Homme'
        return sexe

    def update_classement(self, new_classement: int):
        """
        Methode pour mettre a jour le classement
        """
        self.elo = new_classement
        self.update_player()

    def win(self):
        self.point += 1
        self.update_player()

    def equality(self):
        self.point += 0.5
        self.update_player()

    def add_meet(self, player: str):
        self.has_met.append(player)
        self.update_player()

    def switch_player_tournament(self):
        """Change le status du joueur dans le tournoi
        Change the status of the players in the tournament
        """
        if self.status:
            self.status = False
        else:
            self.status = True

        p = []
        Player._NB_ACTIVE_PLAYERS = len([p.append(player) for player in Player._PLAYERS if player.status])
        self.update_player()

    @classmethod
    def isactiveplayerlistpair(cls):
        """Method to find out if the list of active players is an even one
        Method permettant de savoir si la liste des joueurs actifs est pair
        """
        cls.list_player_tournament()
        if cls._NB_ACTIVE_PLAYERS % 2:
            return False                 # Impair
        else:
            return True                  # Paire

    @classmethod
    def initialise_players_data(cls):
        """ Class method call for initialize Tournament and reset old point and meet between players."""

        q = Query()

        players_table = cls.__db

        players_table.update_multiple([
                ({'point': 0}, q.point.exists()),
                ({'has_met': []}, q.has_met.exists())
        ])

        # ({'status': False}, q.status.exists()),

        # p = [player for player in cls._PLAYERS if player.point != 0]
        #
        # for player in p:
        #     player.point = 0
        #
        # p = [player for player in cls._PLAYERS if len(player.has_met)]
        #
        # for player in p:
        #     player.has_met.clear()
        #
        # p = [player for player in cls._PLAYERS if player.status]
        #
        # for player in p:
        #     player.switch_player_tournament()
        #
        # cls.save_all_players()

    @classmethod
    def list_all_player(cls):
        var = [player for player in cls._PLAYERS]
        return var

    @classmethod
    def list_player_tournament(cls) -> list:
        var = [player for player in cls._PLAYERS if player.status]
        cls._NB_ACTIVE_PLAYERS = len(var)
        return var

# --------------------------TinyDB parts---------------------------------------
    @classmethod
    def save_all_players(cls):
        """
        Methode de classe permettant de sauvegarder l'ensemble des joueurs.
        Class method allowing all players to be saved.
        """
        players_db = cls.__db
        players_db.truncate()
        serialized_players = [cls.player.__serialize_player() for cls.player
                              in cls._PLAYERS]
        players_db.insert_multiple(serialized_players)

    def __serialize_player(self):
        data = self.__dict__
        return data

    @classmethod
    def load_players(cls):
        """
        Methode de classe permettant de charger l'ensemble des joueurs connus.

        Class method allowing all players to be loaded.
        """
        serialized_players_list = cls.__db.all()
        [Player(**data) for data in serialized_players_list]



if __name__ == '__main__':
    Player.load_players()
    Player.list_all_player()
    print("heu....")
    Player.initialise_players_data()