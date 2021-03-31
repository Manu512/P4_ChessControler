""" Model Player """
# coding: utf-8

from datetime import datetime as dt
from typing import Any
from uuid import uuid4

from tinydb import Query, TinyDB


class Player:
    """
    Class that will manage all the players. Participating or not in the tournament.

    Classe qui va gérer l'ensemble des joueurs. Participant ou non au tournoi.
    """

    __db = TinyDB('players.json', sort_keys=True, indent=4, separators=(',', ': '))
    __db = __db.table('players')

    NB_PLAYER: int = 0
    NB_ACTIVE_PLAYERS: int = 0
    PLAYERS: list[Any] = []

    def __new__(cls, **kwargs):
        if 'uuid' in kwargs:
            for player in cls.PLAYERS:
                if player.uuid == kwargs['uuid']:
                    return None
        self = super().__new__(cls)
        self.PLAYERS.append(self)
        return self

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.first_name = kwargs['first_name']
        self.dob = kwargs['dob']
        self._genre = kwargs['_genre']
        self.elo = 0
        self.point = 0
        self.has_met = []
        self.status = False
        Player.NB_PLAYER = Player.NB_PLAYER + 1
        self.id = Player.NB_PLAYER
        self.uuid = str(uuid4())

        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)

    def __repr__(self):
        return "{} ({} ans) - Elo : {}".format(self.fullname, self.age, self.elo)

    def update_player(self):
        """
        Method of saving player information (creation or update)
        Methode de sauvegarde des informations joueurs (création ou mise à jour)
        """
        q = Query()
        players_table = self.__db
        player_data = self.serialize_player()
        players_table.upsert(player_data, q.uuid == self.uuid)

    @classmethod
    def all_players_inactive(cls):
        """
        Methode pour désinscrire tous les joueurs du tournoi
        """
        [player.switch_player_tournament() for player in cls.PLAYERS if player.status]

    @property
    def age(self) -> int:
        """
        Property for calculating age using the date of birth.
        """
        birth = dt.strptime(self.dob, '%d/%m/%Y')
        today = dt.today()
        return today.year - birth.year - (
                    (today.month, today.day) < (birth.month, birth.day))

    @property
    def fullname(self):
        """
        Property displaying the first and last name of the player.
        """
        return f"{self.name} {self.first_name}"

    @property
    def sexe(self) -> str:
        """
        Property to display the gender in a readable way
        """
        if self._genre == 'F':
            sexe = 'Femme'
        else:
            sexe = 'Homme'
        return sexe

    def update_classement(self, new_ranking: int):
        """
        Method to update the ranking
        """
        self.elo = new_ranking
        self.update_player()

    def win(self):
        """
        Method for adding victory points
        """
        self.point += 1
        self.update_player()

    def equality(self):
        """
        Method for adding points in case of a tie
        """
        self.point += 0.5
        self.update_player()

    def add_meet(self, player: str):
        """
        Method for adding the ID of an opponent that has been encountered
        in the attribute self.has_met

        :param player: str id of the opponent.
        """
        self.has_met.append(player)
        self.has_met = list(set(self.has_met))

    def switch_player_tournament(self):
        """Change le status du joueur dans le tournoi
        Change the status of the players in the tournament
        """
        if self.status:
            self.status = False
        else:
            self.status = True
        self.count_active_players()
        self.update_player()

    @classmethod
    def count_active_players(cls):
        p = []
        cls.NB_ACTIVE_PLAYERS = len([p.append(player) for player in cls.PLAYERS if player.status])

    @classmethod
    def isactiveplayerlistpair(cls) -> bool:
        """
        Method to find out if the list of active players is even
        """
        cls.list_player_tournament()
        if cls.NB_ACTIVE_PLAYERS % 2:
            ret = False                 # Odd
        else:
            ret = True                  # Pair

        return ret

    @classmethod
    def initialise_players_data(cls):
        """
        Class method call for initialize Tournament and reset old point and meet between players.
        """
        q = Query()

        players_table = cls.__db

        players_table.update_multiple([
                ({'point': 0}, q.point.exists()),
                ({'has_met': []}, q.has_met.exists())
        ])

        for player in cls.PLAYERS:
            player.point = 0
            player.has_met = []

    @classmethod
    def list_all_player(cls) -> list:
        """
        Class method that returns the list of all instantiated players.
        """
        return cls.PLAYERS

    @classmethod
    def list_player_tournament(cls) -> list:
        """
        Class method returning a list of player objects with an active status
        :return: list of the registered players
        """

        ret = [player for player in cls.PLAYERS if player.status]
        cls.count_active_players()
        return ret

# --------------------------TinyDB parts---------------------------------------
    @classmethod
    def save_all_players(cls):
        """
        Methode de classe permettant de sauvegarder l'ensemble des joueurs.
        Class method allowing all players to be saved.
        """
        players_db = cls.__db
        players_db.truncate()
        serialized_players = [cls.player.serialize_player() for cls.player
                              in cls.PLAYERS]
        players_db.insert_multiple(serialized_players)

    def serialize_player(self) -> dict:
        """
        Method to return the set of arguments as a dictionary
        :return: dict
        """
        data = self.__dict__
        return data

    @classmethod
    def load_players(cls):
        """
        Class method for loading all known players.
        """
        serialized_players_list = cls.__db.all()
        [Player(**data) for data in serialized_players_list]
        cls.count_active_players()
