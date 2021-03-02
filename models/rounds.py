# coding: utf-8

import datetime as dt
from uuid import uuid4

from .players import Player

class Round:
    """Contient les informations Date de debut et de fin, et listes des matchs à venir"""
    N_ROUND = 0
    MAX_ROUND = 8

    def __init__(self, players):
        Round.N_ROUND += 1
        self.id = str(uuid4())
        self.name = 'Round {}'.format(Round.N_ROUND)
        self.start = dt.datetime.now()
        self.end = ''
        self.matchs = []
        self.players = players

    def __repr__(self):
        return self.name

    def add_match(self, match):
        """

        :param tuple match: tuple provenant d'un objet Match
        """
        self.matchs.append(match)

    def end_round(self):
        """

        Method called at end of round
        """
        self.end = dt.datetime.now()

    def sort_player(self, players) -> list:
        players.sort(reverse=True, key=lambda x: (x.point, x.elo))
        return players

    def already_played(self, players) -> bool:
        """
        Permet de retourner un bool sur le fait d'avoir deja jouer contre l'adversaire.
        """
        #if
        return state

    def define_matchs_in_round(self) -> list:
        nb_joueur = len(self.players)
        if self.round_number == 1:
            players_list_1 = []
            players_list_2 = []
            self.players = self.sort_player(self.players)
            nb_joueur = len(self.players)
            if len(players_list_1) % 2 == 0:
                players_list_1 = self.players[:nb_joueur // 2]
                players_list_2 = self.players[nb_joueur // 2):]

                first_round = list(zip(players_list_1, players_list_2))
                return first_round

            else:
                print("Il manque un joueur pour générer toutes les paires")
                """a retoucher dans controler et players"""


        else:
            self.sort_player(self.players)
            other_round = []
            for x in range(0, nb_joueur, 2):
                """ Penser a utiliser la fonction 
                sur la 1° liste pour retirer les versus de player.versus. 


                """
                other_round.append((self.players[x], self.players[x + 1]))
            return other_round

    def display_match(self):
        """
        Method display match informations
        """
        print("\n{0} Début: {1} Fin: {2}".format(self.name, self.start,
                                                 self.end, ))
        for nb in range(len(self.matchs)):
            print("{0} {1} VS {2} {3}".format(self.matchs[nb][0][0],
                                              self.matchs[nb][0][1],
                                              self.matchs[nb][1][1],
                                              self.matchs[nb][1][0]))

if __name__ == '__main__':
    joueurs_factice = [Player(name='WALDNER', first_name='Emmanuel', date_of_birth='18/06/1980', sexe=0, elo=1200),
                       Player(name='BREDERECK', first_name='Estelle', date_of_birth='05/07/1980', sexe=1, elo=1000),
                       Player(name='WALDNER', first_name='Bernard', date_of_birth='26/01/1950', sexe=0, elo=800),
                       Player(name='WALDNER', first_name='Eliane', date_of_birth='18/04/1953', sexe=1, elo=900),
                       Player(name='BREDERECK', first_name='Leon', date_of_birth='22/07/1956', sexe=0, elo=1200),
                       Player(name='WALDNER', first_name='Raphael', date_of_birth='17/07/2018', sexe=0, elo=1200),
                       Player(name='PFIRSCH', first_name='Bernadette', date_of_birth='03/05/1959', sexe=1, elo=1050),
                       Player(name='WITZ', first_name='Manuel', date_of_birth='05/08/1971', sexe=0, elo=1150)]

    joueurs_factice[3].point = 15
    joueurs_factice[2].point = 10
    joueurs_factice[0].point = 15
    round = Round()
    round = round.define_matchs_in_round()
    print(round)