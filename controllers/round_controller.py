"""Round Controller"""
# coding: utf-8
from controllers.controller import *


class RoundController(BaseController):

    def __init__(self, tournament: Tournoi):
        super().__init__()
        self.tournament = tournament
        self.round = tournament.rounds[-1]
        self.menu_round()

    def menu_round(self):
        """
        Menu de gestion des rounds
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec.\n"
        subtitle = "Console de gestion des rounds du tournoi."
        menu = {1: (self.menu_round, f"Nom : {self.round.name}"),
                2: (self.menu_round, f"Début du Round : {self.round.start}"),
                3: (self.stop_round, f"Fin du Round : {self.round.end}"),
                4: (self.list_round_matchs, 'Consulter les matches en cours'),
                5: (self.add_score, f"Saisir les scores du Round {self.round.number}"),
                6: (self.start_new_round, 'Démarrer nouveau Round'),
                7: (Controller.menu_tournament, 'Retour au menu')}

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        self.ask_and_launch(menu=menu)

    def list_round_matchs(self):
        if self.round.number != 0:
            self.view_menu.view_matchs(self.round)
        else:
            self.view_menu.error_msg("Commencer par démarrer un round !!!!")

        self.input_press_continue()
        self.menu_round()

    def add_score(self):
        if self.round.number != 0:
            self.view_menu.select_match(self.round.matches[-1])
            response = self.ask_and_launch("Choisissez le match pour renseigner le résultat :")

            if self.check_match_choice(response):
                match_played = self.round.matches[int(response) - 1]
                self.view_menu.select_winner(match_played)
                response = self.ask_and_launch()

                if int(response) in [1, 2]:
                    match_played.players[int(response) - 1].win()
                    match_played.win(match_played.players[int(response) - 1])
                    print(f"Le gagnant est !!!! {match_played.players[int(response) - 1]}")
                else:
                    match_played.players[0].equality()
                    match_played.players[1].equality()
                    match_played.win()
                    print(f"Equality !!!!!")

                match_played.players[0].add_meet(match_played.players[1].uuid)
                match_played.players[1].add_meet(match_played.players[0].uuid)

                return

        else:
            self.view_menu.error_msg("Commencer par démarrer un round !!!!")

    def start_new_round(self):
        """Si l'ancien round n'est pas fini ==> Erreur"""
        if self.round.start != "" and self.round.end == "":
            self.view_menu.error_msg("Attention, le précédent round n'est pas fini !")
            self.input_press_continue()
        else:
            self.round.new_round()

    def stop_round(self):
        if self.round.start != "":
            self.round.end_round()
        else:
            self.view_menu.error_msg("Commencer par démarrer un round !!!!")
            self.input_press_continue()

    def check_match_choice(self, response: int) -> bool:
        if len(str(response)) != 1:
            self.view_menu.error_msg("Choix incorrect. Un chiffre demandé."
                                     " Veuillez ressaisir !")
            self.input_press_continue()
            return False
        elif int(response) not in [1, 2, 3, 4]:
            self.view_menu.error_msg("Choix incorrect !! Veuillez ressaisir")
            self.input_press_continue()
            return False
        else:
            return True
