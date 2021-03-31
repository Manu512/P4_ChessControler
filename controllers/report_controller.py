""" Report Menu Controller"""
# coding:utf-8

from controllers import BaseController
from models.players import Player


class ReportController(BaseController):
    """
    Objective To enable reporting with tournament data.

    """

    def __init__(self, tournament):
        super().__init__(tournament)

    def menu_rapport(self):
        """
        Method for displaying the report management menu
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Page d'édition des rapports"
        menu = {1: (self.list_all_players_sort_alpha, "Liste de tous les joueurs classé par ordre alphabétique"),
                2: (self.list_all_players_sort_elo, "Liste de tous les joueurs classé selon ELO"),
                3: (self.list_tournament_players_sort_alpha, "Liste de tous les joueurs d'un tournoi"
                                                             " classé par ordre alphabétique"),
                4: (self.list_tournament_players_sort_elo, "Liste de tous les joueurs d'un tournoi classé selon"),
                5: (self.list_tournaments, "Liste de tous les tournois"),
                6: (self.list_all_rounds, "Liste de tous les tours du tournoi"),
                7: (self.list_all_matchs, "Liste de tous les matchs du tournoi"),
                9: (str('back'), 'Retour au menu')}

        if self.tournament is None:
            del menu[6]
            del menu[7]

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        r = self.ask_and_launch(menu=menu)

        return self.back_menu(r)

    # --------------------------RAPPORT METHODS------------------------------------

    def list_all_players_sort_alpha(self):
        """
        Function that will print the list of known players sorted alphabetically
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Listing des joueurs :"
        data = Player.list_all_player()
        data.sort(key=lambda x: (x.name, x.first_name))
        self.view_menu.display_data(title, subtitle, data)

    def list_tournament_players_sort_alpha(self):
        """
        Function that will print the list of players in the tournament sorted alphabetically
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Listing des joueurs du tournoi :"
        data = Player.list_player_tournament()
        data.sort(key=lambda x: (x.name, x.first_name))
        self.view_menu.display_data(title, subtitle, data)

    def list_all_players_sort_elo(self):
        """
        Function that will print the list of known players sorted by ELO
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Listing des joueurs :"
        data = Player.list_all_player()
        data.sort(reverse=True, key=lambda x: int(x.elo))
        self.view_menu.display_data(title, subtitle, data)

    def list_tournament_players_sort_elo(self):
        """
        Function that will print the list of players in the tournament sorted by ELO
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Listing des joueurs du tournoi :"
        data = Player.list_player_tournament()
        data.sort(reverse=True, key=lambda x: int(x.elo))
        self.view_menu.display_data(title, subtitle, data)

    def list_tournaments(self):
        """
        Function that will print the list of tournaments
        """
        data = self.load_saved_tournament()
        subtitle = 'Liste des tournois sauvegardés'
        self.view_menu.view_saved_tournament(subtitle, data=data)
        self.view_menu.stand_by_msg()

    def list_all_rounds(self):
        """
        Fonction qui va lancer le print de tous les rounds du tournois
        """
        self.view_menu.report_round_tournament(data=self.tournament.rounds)
        self.view_menu.stand_by_msg()

    def list_all_matchs(self):
        """
        Fonction qui va lancer le print de la liste des matches du tournois
        """
        self.view_menu.report_matches_tournament(data=self.tournament.rounds)
        self.view_menu.stand_by_msg()
