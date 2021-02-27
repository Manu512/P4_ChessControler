# coding: utf-8
from tinydb import TinyDB
from datetime import datetime as dt


class Player:

    NB_PLAYER = 0
    PLAYERS = []

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        Player.NB_PLAYER = self.id
        self.name = kwargs['name']
        self.first_name = kwargs['first_name']
        self.dob = kwargs['dob']
        self._genre = kwargs['sexe']
        self.elo = kwargs['elo']
        self.point = kwargs['score']
        self.versus = kwargs['versus']
        self.status = kwargs['status']
        Player.PLAYERS.append(self)

    def __repr__(self):
        return "{} {} - elo : {} - Pts : {} - Engagé : {}".format(self.name,
                                                                  self.first_name,
                                                                  self.elo,
                                                                  self.point,
                                                                  self.status)

    @property
    def age(self) -> int:
        today = dt.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    @property
    def sexe(self) -> str:
        if self._genre:
            sexe = 'Femme'
        else:
            sexe = 'Homme'
        return sexe

    def update_classement(self, new_classement: int):
        self.elo = new_classement

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
        self.data = {"id": self.id,
                     "name": self.name,
                     "first_name": self.first_name,
                     "dob": self.dob,
                     "sexe": self.sexe,
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
    # joueurs_factice = [Player(name='WALDNER', first_name='Emmanuel', date_of_birth='18/06/1980', sexe=0, elo=1200),
    #                    Player(name='BREDERECK', first_name='Estelle', date_of_birth='05/07/1980', sexe=1, elo=1000),
    #                    Player(name='WALDNER', first_name='Bernard', date_of_birth='26/01/1950', sexe=0, elo=800),
    #                    Player(name='WALDNER', first_name='Eliane', date_of_birth='18/04/1953', sexe=1, elo=900),
    #                    Player(name='BREDERECK', first_name='Leon', date_of_birth='22/07/1956', sexe=0, elo=1200),
    #                    Player(name='WALDNER', first_name='Raphael', date_of_birth='17/07/2018', sexe=0, elo=1200),
    #                    Player(name='PFIRSCH', first_name='Bernadette', date_of_birth='03/05/1959', sexe=1, elo=1050),
    #                    Player(name='WITZ', first_name='Manuel', date_of_birth='05/08/1971', sexe=0, elo=1150)]


    # self.players_db.truncate()
    # serialized_players = [p.save_player() for player in players]
    # player_data.insert_multiple(serialized_players)
    # db = TinyDB('players.json')
    # players_db = db.table('players')
    # players_db.truncate()
    # serialized_players = [player.save_player() for player in Player.PLAYERS]
    # players_db.insert_multiple(serialized_players)

    Player.load_players()
    Player.list_all_player()
    print("heu....")
