# coding: utf-8
from datetime import datetime as dt
from uuid import uuid4

from tinydb import Query, TinyDB

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

        if isinstance(timer, str) and timer is not None:
            self.timer = timer
        else:
            self.timer = self.TIMER

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
            r = {'id': round.id, 'name': round.name, 'number': round.number, 'start': round.start, 'end': round.end}
            data_round.append(r)
            data_players = []
            for player in round.players:
                player_data = player.uuid, player.point, player.has_met
                data_players.append(player_data)
            data_matches = []
            for match in round.matches:
                if isinstance(match.score, list):
                    match_serialize = ([match.players[0].uuid, match.players[1].uuid], [match.score[0], match.score[1]])
                else:
                    match_serialize = ([match.players[0].uuid, match.players[1].uuid], None)
                data_matches.append(match_serialize)
            data_round.append({"matches": data_matches})
            data["players"] = data_players
        data["rounds"] = data_round
        self.table_tournoi.upsert(data, q.id == self.id)
        return self

    @classmethod
    def load(cls):
        """Methode de chargement d'un tournoi sauvegarde
        """
        Player.initialise_players_data()
        data_load = cls.table_tournoi.all()

        data_load = data_load[-1]

        t = {}
        # --------- Load Objet Tournament ----------

        t['identity'] = data_load['id']
        t['name'] = data_load['name']
        t['location'] = data_load['location']
        t['tournament_date'] = data_load['tournament_date']
        t['timer'] = data_load['timer']
        t['description'] = data_load['description']
        t['rounds_number'] = data_load['rounds_number']

        tournament = Tournoi(t['identity'],
                             t['name'],
                             t['location'],
                             t['tournament_date'],
                             t['description'],
                             t['timer'],
                             rounds_number=t['rounds_number'])

        # --------- Load Objet Player ---------------

        t['players'] = data_load['players']
        for player in t['players']:
            """
            1 - On recherche le joueur ayant uuid stocker en player[0]
            2 - On lui affecte le nombre de point stocker en player[1]
            3 - On renseigne les rencontres existantes stocker en player[2]
            """
            p_found = [p for p in Player._PLAYERS if player[0] == p.uuid]

            assert p_found          # Leve une exception si le joueur n'est pas trouvé

            p_found = p_found[0]

            # p_found.switch_player_tournament()
            p_found.point = player[1]
            for meet in player[2]:
                p_found.add_meet(meet)

        # --------- Load Objet Round ----------------

        t['rounds'] = data_load['rounds']
        for n, round in enumerate(t['rounds']):
            """
            1 - On balaye les rounds sauvegardés.
            2 - On extrait les infos du rounds.
            3 - On extraits les matchs et les scores.
            """
            if n % 2 == 0:
                tournament.rounds.append(Round(round['number'],
                                         Player.list_player_tournament(),
                                         round['start'],
                                         round['end'],
                                         t['rounds'][n+1]['matches'],
                                         round['id']))

        # --------- On crée les objets tournoi, rounds, matches avec les infos récupérées
        return tournament

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
        """
        Contrôle du nombre de joueur selectionné pour le tournoi
        """
        r = Round(round_number=self.rounds_number + 1, players=player)
        self.rounds.append(r)
        self.rounds_number += 1
        return

    @property
    def current_round(self):
        return self.rounds[-1].name
