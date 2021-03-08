# coding: utf-8
import json
from datetime import datetime as dt
from uuid import uuid4

from tinydb import Query, TinyDB
import pickle

from models.rounds import Round
from models.players import Player


class Tournoi:

    __db = TinyDB('tournament.json')
    table_tournoi = __db.table('tournament')

    NAME = "Tournoi d'échec"
    NB_ROUND = 4
    NB_DEFAULT_PLAYERS = 8
    TIMER = "Bullet"
    DESCRIPTION = ""
    LOCATION = 'France'

    def __init__(self, identity: str = None, name: str = "Tournoi d'échec", location: str = None,
                 tournament_date: str = None, description: str = None,
                 timer: str = TIMER, rounds: list[Round] = None, rounds_number: int = None):

        if isinstance(identity, str) and identity is not None:
            self.id = identity
        else:
            self.id = str(uuid4())

        self.name = name

        if isinstance(location, str) and location is not None:
            self.location = location
        else:
            self.location = self.LOCATION

        if isinstance(tournament_date, str) and tournament_date is not None:
            self.tournament_date = tournament_date
        else:
            self.tournament_date = dt.now().date().strftime("%Y-%m-%d")

        self.timer = timer

        if isinstance(description, str) and description is not None:
            self.description = description
        else:
            self.description = self.DESCRIPTION
        self.rounds = []

        if rounds_number:
            self.rounds_number = rounds_number
        else:
            self.rounds_number = 0

        if rounds:
            for data in rounds:
                round = Round(**data)
                self.rounds.append(round)

    def save(self):
        """ Methode de sauvegarde des données au format JSON avec TinyDB"""
        q = Query()

        data = self.__dict__.copy()
        del data["rounds"]

        data_round = []
        for round in self.rounds:
            r = [round.id, round.name, round.number, round.start, round.end]
            data_round.append(r)





        self.table_tournoi.upsert(data, q.id == self.id)

        return self

    def __repr__(self):
        return self.name + " - " + self.id

    def set_timer_bullet(self):
        self.timer = "Bullet"

    def set_timer_fast(self):
        self.timer = "Coup Rapide"

    def set_timer_blitz(self):
        self.timer = "Blitz"

    def add_round(self):
        player = Player.list_player_tournament()
        r = Round(round_number=self.rounds_number + 1, players=player)
        self.rounds.append(r)
        self.rounds_number += 1
        return

    @property
    def current_round(self):
        return self.rounds[-1].name

    @classmethod
    def load_tournament(cls):
        # TODO A faire
        """
        Methode de classe permettant de charger l'ensemble des joueurs connus.

        Class method allowing all players to be loaded.
        """
        serialized_tournament_data = cls.table_tournoi.all()
        [Tournoi(**data) for data in serialized_tournament_data]
