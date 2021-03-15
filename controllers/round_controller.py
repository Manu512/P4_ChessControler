"""Round Controller"""
# coding: utf-8


from controllers import BaseController

from models.tournoi import Tournoi


class RoundController(BaseController):

    def __init__(self, tournament: Tournoi):
        super().__init__(tournament)
        # self.tournament = tournament
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
                9: (self.back_menu, 'Retour au menu')}

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        self.ask_and_launch(menu=menu)
        if self.back_menu():
            pass
        else:
            self.menu_round()

    def back_menu(self):
        return True

    def list_round_matchs(self):
        self.view_menu.view_matchs(self.round)
        self.input_press_continue()
        self.menu_round()

    def add_score(self):
        self.view_menu.select_match(self.round)
        response = self.ask_and_store_number("Choisissez le match pour renseigner le résultat :")
        """
        response = tuple(False/True if valid input, input value)
        """
        if response[0]:
            match_played = self.round.matches[response[1]-1]
            self.view_menu.select_winner(match_played)
            response = self.ask_and_store_number()

            if response[1] in [1, 2]:
                match_played.players[response[1]-1].win()
                match_played.win(match_played.players[response[1]-1])
                print(f"Le gagnant est !!!! {match_played.players[response[1]-1]}")
            else:
                match_played.players[0].equality()
                match_played.players[1].equality()
                match_played.win()
                print("Equality !!!!!")
            match_played.players[0].add_meet(match_played.players[1].uuid)
            match_played.players[1].add_meet(match_played.players[0].uuid)


    def start_new_round(self):
        """Si l'ancien round n'est pas fini ==> Erreur"""
        if self.round.start != "" and self.round.end == "":
            self.view_menu.error_msg("Attention, le précédent round n'est pas fini !")
            self.input_press_continue()
        else:
            self.tournament.add_round()
            self.round = self.tournament.rounds[-1]

    def stop_round(self):
        if self.round.start != "":
            self.round.end_round()
        else:
            self.view_menu.error_msg("Commencer par démarrer un round !!!!")
            self.input_press_continue()

        self.menu_round()
